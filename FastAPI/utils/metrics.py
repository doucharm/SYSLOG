from prometheus_client import Counter,Histogram
#Set up Prometheus metrics to monitor the traffic
server_request_total = Counter("server_request_total","Number of requests")
server_fail_request_total = Counter("server_fail_request_total","Number of failed requests")
server_response_time_ms = Histogram('server_response_time_ms',"Wait time for request sent",buckets=[0,5,10,15,20,25,30,40,50,65,80,100,250,500,1000,2500])
server_reponse_length_bytes = Histogram('server_reponse_length_bytes','The length of the response from database',buckets=[0,50,100,250,500,750,1000,2000,3500,5000])
server_authentication_rejected_total=Counter('server_authentication_rejected_total','How many request are rejected by the API due to problem with authentication')

webpage_referer_total=Counter('webpage_referer_total','Number of request comming from a webpage',['referer'])

#Metrics for each client
client_request_total = Counter("client_request_total",'Number of request coming from a client',['client','method'])
client_success_response_total=Counter('client_success_response_total','Number of success request coming from a client',['client','media_type'])

mime_types=['application','audio','text','image','video','etc']
methods=['GET','POST']
origins=[]
for origin in origins:
    for method in methods:
        client_request_total.labels(client = origin,method=method)
    for media in mime_types:
        client_success_response_total.labels(client = origin,media_type=media)
def new_prometheus_origin(origin):
    for method in methods:
        client_request_total.labels(client = origin,method=method)

    for media in mime_types:
        client_success_response_total.labels(client = origin,media_type=media)   
def add_prometheus_referer(referer):

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
        print(request_duration*1000)
        server_reponse_length_bytes.observe(int(respone_length))
        server_response_time_ms.observe(request_duration*1000)
    else:
        server_fail_request_total.inc()
    #Webpage specific mettrics handler
    if referer:
        add_prometheus_referer(referer)
    #Change metrics for client that made the request
    client_request_total.labels(origin,method).inc()
    if success :
         client_success_response_total.labels(origin,media_type).inc()


