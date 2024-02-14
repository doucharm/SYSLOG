import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app,generate_latest
import time
from utils.syslog_exporter import logger,request_log
from utils.metrics import increase_count,query_returned_length,query_waiting_time
from utils.variables import database_ip,origins,status_block
from tokens.DBModel import ComposeConnectionString,startEngine
from utils.token_records import process_token,check_token_validity
from utils.user_record import process_user
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
    user_id=headers['user_id']
    return [bearer_token,request_ip,user_id]
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
graphql_app = GraphQLRouter(schema,context_getter=get_context)
app.include_router(graphql_app, prefix="/tokens/gql") #graphiql na testování 
metrics=make_asgi_app() #vytvořit Prometheus instance na sledování a zasílaní dat sledování do dedikační Prometheus serveru
app.mount("/metrics",metrics)
class Item( BaseModel ):
    query: str
    variables: dict = None
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
#sentinel=authenticationMiddleware.createAuthentizationSentinel()
@app.post("/gql", response_class=JSONResponse)
async def GQL_Post(data: Item, request: Request):
    #sentinel.authenticate(request=request)
    sessionMaker = await startEngine(ComposeConnectionString(),False,True) #funkce na vytvoření pracovní sekce s tabulkkami
    bearer_token=None
    request_ip=None
    user_id=None
    status_code=[400]
    [bearer_token,request_ip,user_id]=GetHeaderData(request.headers) #sbírat potřebné informace ze dotazní záhlaví
    if await check_token_validity(session=sessionMaker(),bearer_token=bearer_token,ip_address=request_ip,status_code=status_code): #provedení kontroly živostnost a zdroje JWT
        time_start=time.time()
        gqlQuery = {"query": data.query}
        gqlQuery["variables"] = data.variables #formulovat další kopie přijetého dotazu 
        increase_count(request.headers['origin']) #Prometheus monitorování
        json=None
        response=None
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(database_ip, json=gqlQuery, headers={}) as resp: #vysílat dotaz dále do vnitřní databáze
                    json = await resp.json()
                    time_end=time.time()
                    query_waiting_time.observe(time_end-time_start)
                response=JSONResponse(content=json, status_code=resp.status)
            except Exception as e:
                response=JSONResponse(content=json, status_code=500) #v případě se nedosahnout do serveru
        response_length=int({key.decode('utf-8'): value.decode('utf-8') for key, value in response.raw_headers}.get('content-length'))
        query_returned_length.observe(response_length)
        if bearer_token is not None: 
            async with sessionMaker() as session: 
                await process_user(session=session,user_id=user_id)     
                await process_token(session=session,bearer_token=bearer_token,status=response.status_code,response_length=response_length,first_ip=request_ip,user_id=user_id)
        if( response.status_code!=200):
            request_log(bearer_token=bearer_token,ip_address=request_ip,status_code=response.status_code)
            return JSONResponse(content=json,status_code=418 if str(status_block)=='True' else response.status_code)
       
        return response
    else: 
        request_log(bearer_token=bearer_token,ip_address=request_ip,status_code=status_code[0])
        response=JSONResponse(content=None,status_code=418 if str(status_block)=='True' else status_code[0])
        return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain')


