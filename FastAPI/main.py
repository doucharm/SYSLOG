import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app,generate_latest
import time
from utils.syslog_exporter import logger
from utils.metrics import https_post_request_count,https_request_count,query_returned_length,query_waiting_time,frequency_access_from_origin
from utils.origins import origins
from utils.proxy import proxy
from utils.token_records import ComposeConnectionString,startEngine,process_token
from strawberry.fastapi import GraphQLRouter
from tokens.GQL_Models import schema

from contextlib import asynccontextmanager

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):
    connectionstring = ComposeConnectionString()
    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )
    appcontext["asyncSessionMaker"] = asyncSessionMaker
    yield
app = FastAPI(lifespan=initEngine)
import sys
for items in sys.path:
    print(items)
def get_context():
    from tokens.utils.Resolvers import createLoadersContext
    return createLoadersContext(appcontext["asyncSessionMaker"])
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)
app.include_router(graphql_app, prefix="/tokens/gql")
metrics=make_asgi_app()
app.mount("/metrics",metrics)
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
    sessionMaker = await startEngine(ComposeConnectionString(),False,True)
    if len(request.headers['authorization']) > 7:
        bearer_token=request.headers['authorization'][7:]
    #logger.warning(request.headers.__dict__)
    time_start=time.time()
    gqlQuery = {"query": data.query}
    gqlQuery["variables"] = data.variables
    info=Info(request.method,request.url,request.headers["origin"],request.client.port)
    https_request_count.inc()
    https_post_request_count.inc()
    frequency_access_from_origin.labels(info.client).inc()
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy, json=gqlQuery, headers={}) as resp:
            json = await resp.json()
            time_end=time.time()
            query_waiting_time.observe(time_end-time_start)
    response=JSONResponse(content=json, status_code=resp.status)
    response_length=int({key.decode('utf-8'): value.decode('utf-8') for key, value in response.raw_headers}.get('content-length'))
    print(response_length)
    query_returned_length.observe(response_length)
    async with sessionMaker() as session:        
        await process_token(session=session,bearer_token=bearer_token,status=resp.status,response_length=response_length)
    return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain'
    )


