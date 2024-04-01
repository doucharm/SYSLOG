from prometheus_client import Counter,Histogram
#Set up Prometheus metrics to monitor the traffic
server_request_total = Counter("server_request_total","Number of requests")
server_fail_request_total = Counter("server_fail_request_total","Number of failed requests")
server_response_time_seconds_bucket = Histogram('server_response_time_seconds_bucket',"Wait time for request sent",buckets=[0,0.1,0.2,0.3,0.4,0.5,0.75,1,2,5])
server_reponse_length_bytes_bucket = Histogram('server_reponse_length_bytes_bucket','The length of the response from database',buckets=[0,100,200,400,500,750,1000,2000,3000,4000,5000])
server_authentication_rejected_total=Counter('server_authentication_rejected_total','How many request are rejected by the API due to problem with authentication')

webpage_referer_total=Counter('webpage_referer_total','Number of request comming from a webpage',['referer'])

#Metrics for each client
client_request_total = Counter("client_request_total",'Number of request coming from a client',['client','method'])
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
    if success:
        server_reponse_length_bytes_bucket.observe(int(respone_length))
        server_response_time_seconds_bucket.observe(int(request_duration))
    
    #Webpage specific mettrics handler
    if referer:
        add_prometheus_referer(referer)

        
    #Change metrics for client that made the request
    client_request_total.labels(origin,method).inc()
    if success :
         client_success_response_total.labels(origin,media_type).inc()


