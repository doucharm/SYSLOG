from prometheus_client import Counter,Histogram
https_request_count = Counter("request_count","Number of requests")
https_post_request_count = Counter("post_count","Number of post requests")
fail_request_count = Counter("fail_count","Number of failed requests")
query_waiting_time = Histogram('query_time',"Wait time for request sent")
query_returned_length = Histogram('query_length','The length of the response from database',buckets=[0,100,200,400,500,750,1000,2000,3000,4000,5000])


frequency_access_from_origin = Counter("frequency_access_from_origin",'Number of request coming from a client',['client'])
from .origins import origins
for origin in origins:
    frequency_access_from_origin.labels(client = origin)
