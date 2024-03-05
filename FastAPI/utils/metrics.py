from prometheus_client import Counter,Histogram
# Nastavit metriky na meření dotazů do databáze
server_request_total = Counter("server_request_total","Number of requests")
server_post_request_total = Counter("server_post_request_total","Number of post requests")
server_fail_request_total = Counter("server_fail_request_total","Number of failed requests")
server_average_response_time_seconds = Histogram('server_average_response_time_seconds',"Wait time for request sent")
server_average_reponse_length_byte = Histogram('server_average_response_length_byte','The length of the response from database',buckets=[0,100,200,400,500,750,1000,2000,3000,4000,5000])

webpage_referer_total=Counter('webpage_referer_total','Number of request comming from a webpage',['referer'])

client_request_total = Counter("client_request_total",'Number of request coming from a client',['client','method'])# pro každý zdroje/klienta nastavíme vlastní Counter 
client_success_response_total=Counter('client_success_response_total','Number of success request coming from a client',['client','media_type'])

mime_types=['application','audio','text','image','video','etc']
methods=['GET','POST']
from .variables import origins
for origin in origins:
    for method in methods:
        client_request_total.labels(client = origin,method=method)
    for media in mime_types:
        client_success_response_total.labels(client = origin,media_type=media)
def new_prometheus_origin(origin):
    if not client_request_total.labels(origin):
        for method in methods:
            client_request_total.labels(client = origin,method=method)

    if not client_success_response_total.labels(origin):
        for media in mime_types:
            client_success_response_total.labels(client = origin,media_type=media)   
def add_prometheus_referer(referer):
    if not webpage_referer_total.labels(referer):
        webpage_referer_total.labels(referer)
    webpage_referer_total.labels(referer).inc()
def data_exporter(request_duration:int,
                  respone_length:int,
                  success:bool,
                  origin:str,
                  method:str,
                  media_type:str,
                  referer:str
                 ):
    
    if origin not in origins:
        new_prometheus_origin(origin=origin) #create metrics for this client 
    #Change server metrics 
    server_request_total.inc() 
    server_post_request_total.inc()
    if success:
        server_average_reponse_length_byte.observe(respone_length)
        server_average_response_time_seconds.observe(request_duration)
    
    #Webpage specific mettrics handler
    if referer:
        add_prometheus_referer(referer)

        
    #Change metrics for client that made the request
    client_request_total.labels(origin,method).inc()
    if success :
         client_success_response_total.labels(origin,media_type).inc()


