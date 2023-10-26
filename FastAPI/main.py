import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app,generate_latest
import time

from utils.metrics import https_post_request_count,https_request_count,query_returned_length,query_waiting_time,frequency_access_from_origin
from utils.origins import origins
from utils.proxy import proxy
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



@app.post("/gql", response_class=JSONResponse)
async def GQL_Post(data: Item, request: Request):
    time_start=time.time()
    gqlQuery = {"query": data.query}
    gqlQuery["variables"] = data.variables
    info=Info(request.method,request.url,request.headers["origin"],request.client.port)
    print(info.__dict__,sep="\n")
    https_request_count.inc()
    https_post_request_count.inc()
    frequency_access_from_origin.labels(info.client).inc()
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers={}) as resp:
            json = await resp.json()
            time_end=time.time()
            query_waiting_time.observe(time_end-time_start)
    response=JSONResponse(content=json, status_code=resp.status)
    query_returned_length.observe(int({key.decode('utf-8'): value.decode('utf-8') for key, value in response.raw_headers}.get('content-length')))
    return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain'
    )


