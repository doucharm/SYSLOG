import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app,generate_latest
import time
import utils.variables as variables
from utils.syslog_exporter import logger,request_log
from utils.metrics import increase_count,query_returned_length,query_waiting_time
from utils.variables import database_ip,origins
from tokens.DBModel import ComposeConnectionString,startEngine
from utils.token_records import process_token,check_token_validity
from strawberry.fastapi import GraphQLRouter
from tokens.GQL_Models.Schema import schema
import re
from contextlib import asynccontextmanager
def GetHeaderData(headers):
    pattern = r'^Bearer\s.*'
    if len(headers['authorization']) > 7 and bool(re.match(pattern=pattern,string=headers['authorization'])):
        bearer_token=headers['authorization'][7:]
    if 'X-Forwarded-For' in headers:
        request_ip=headers['X-Forwarded-For']
    else: 
        request_ip=headers['origin']
    return [bearer_token,request_ip]
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
    bearer_token=None
    request_ip=None
    status_code=[400]
    [bearer_token,request_ip]=GetHeaderData(request.headers)
    logger.info("user "+ bearer_token)
    if await check_token_validity(session=sessionMaker(),bearer_token=bearer_token,ip_address=request_ip,status_code=status_code):
        time_start=time.time()
        gqlQuery = {"query": data.query}
        gqlQuery["variables"] = data.variables
        increase_count(request.headers['origin'])
        async with aiohttp.ClientSession() as session:
            async with session.post(database_ip, json=gqlQuery, headers={}) as resp:
                json = await resp.json()
                time_end=time.time()
                query_waiting_time.observe(time_end-time_start)
        response=JSONResponse(content=json, status_code=resp.status)
        if( resp.status!=200):
            request_log(bearer_token=bearer_token,ip_address=request_ip,status_code=resp.status)
            return JSONResponse(content=json,status_code=418 if variables.status_block else resp.status)
        response_length=int({key.decode('utf-8'): value.decode('utf-8') for key, value in response.raw_headers}.get('content-length'))
        query_returned_length.observe(response_length)
        async with sessionMaker() as session:        
            await process_token(session=session,bearer_token=bearer_token,status=resp.status,response_length=response_length,first_ip=request_ip)
        return response
    else: 
        request_log(bearer_token=bearer_token,ip_address=request_ip,status_code=status_code[0])
        response=JSONResponse(content=None,status_code=418 if variables.status_block else status_code[0])
        return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain'
    )


