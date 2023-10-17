import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from permisions import origins
from prometheus_client import make_asgi_app,Counter,generate_latest,Histogram,Summary
import time

app = FastAPI()
metrics=make_asgi_app()
app.mount("/metric",metrics)
class Item(BaseModel):
    query: str
    variables: dict = None
class Info():
    method:str
    url:str
    client:str
    port:str
    def __init__(self, method:str,url:str ,client:str,port:str):
        print(method,url,client,port,sep="  ")
        self.method=method
        self.url=url
        self.client=client
        self.port=port
        


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
request_count = Counter("request_count","Number of requests")
post_count = Counter("post_count","Number of post requests")
fail_count = Counter("fail_count","Number of failed requests")
query_time = Histogram('query_time',"Wait time for request sent")
query_length = Histogram('query_length','The length of the response from database',buckets=[0,100,200,400,500,750,1000,2000,3000,4000,5000])
proxy = "http://localhost:31120/gql" #location of the database

@app.post("/gql", response_class=JSONResponse)
async def GQL_Post(data: Item, request: Request):
    time_start=time.time()
    gqlQuery = {"query": data.query}
    gqlQuery["variables"] = data.variables
    info=Info(request.method,request.url,request.headers["origin"],request.client.port)
    print(info.__dict__,sep="\n")
    request_count.inc()
    post_count.inc()
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers={}) as resp:
            json = await resp.json()
            time_end=time.time()
            query_time.observe(time_end-time_start)
    response=JSONResponse(content=json, status_code=resp.status)
    query_length.observe(int({key.decode('utf-8'): value.decode('utf-8') for key, value in response.raw_headers}.get('content-length')))
    return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain'
    )


