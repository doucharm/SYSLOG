import aiohttp
from typing import Union
from pydantic import BaseModel,HttpUrl
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    query: str
    variables: dict = None
app = FastAPI()
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
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
proxy = "http://localhost:31120/gql" #location of the database
@app.post("/gql", response_class=JSONResponse)
async def GQL_Post(data: Item, request: Request):
    gqlQuery = {"query": data.query}
    gqlQuery["variables"] = data.variables
    headers = request.headers
    ##print("_________________-")
    #print(request.headers.__dict__)
    info=Info(request.method,request.url,request.headers["origin"],request.client.port)
    print(info.__dict__,sep="\n")
    headers = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers={}) as resp:
            json = await resp.json()
    return JSONResponse(content=json, status_code=resp.status)
@app.get("/gql", response_class=JSONResponse)
async def GQL_Get(data: Item, request: Request):
    gqlQuery = {"query": data.query}
    gqlQuery["variables"] = data.variables
    headers = request.headers
    print("header",request.__dict__)
    info=Info(request.method,request.url,request.headers["origin"],request.client.port)
    print(info.__dict__,sep="\n")
    headers = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers={}) as resp:
            json = await resp.json()
            print("res",json)
    return JSONResponse(content=json, status_code=resp.status)


