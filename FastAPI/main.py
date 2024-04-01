import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request,Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app,generate_latest
import time
from utils.syslog_exporter import request_log
from utils.metrics import data_exporter,server_authentication_rejected_total
from utils.variables import database_ip,origins,status_block
from tokens.DBModel import ComposeConnectionString,startEngine
from utils.token_records import process_token,check_token_validity
from utils.user_record import process_user
from utils.header_process import get_request_header_data,get_response_header_data
from strawberry.fastapi import GraphQLRouter
from tokens.GQL_Models.Schema import schema
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

def get_context():
    from tokens.utils.Resolvers import createLoadersContext
    return createLoadersContext(appcontext["asyncSessionMaker"])
graphql_app = GraphQLRouter(schema,context_getter=get_context)
app.include_router(graphql_app, prefix="/tokens/gql") #GraphiQL endpoint provides a viewpoint into the database 
metrics=make_asgi_app() #instrument own's Prometheus 
app.mount("/metrics",metrics)
class Item( BaseModel ):
    query: str
    variables: dict = None #ViolationModel může záznamovat ty variables (id) pokud chce zjíští,kterého objektů útočník požadá informace 
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

#sentinel=authenticationMiddleware.createAuthentizationSentinel()
"""
This function intercept a user's request midway to process before sending a copie of it to the actual database. Reply for the request is then processed and return back to the user
    Params:
        data is the JSON query
        request is the request made by user
    Return:
        Reply from the database
"""
@app.post("/gql", response_class=JSONResponse)
async def GQL_Post(data: Item, request: Request):
    #sentinel.authenticate(request=request)
    sessionMaker = await startEngine(ComposeConnectionString(),False,True) #funkce na vytvoření pracovní sekce s tabulkkami
    status_code=[400]
    req=get_request_header_data(request.headers)
    request_duration=None
    res=None
    if await check_token_validity(session=sessionMaker(),bearer_token=req['bearer_token'],ip_address=req['origin'],status_code=status_code): #provedení kontroly živostnost a zdroje JWT
    
        time_start=time.time()
        gqlQuery = {"query": data.query}
        gqlQuery["variables"] = data.variables 
        json=None
        response=None
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(database_ip, json=gqlQuery, headers={}) as resp:
                    json = await resp.json()
                    time_end=time.time()
                    request_duration=time_end-time_start
                response=JSONResponse(content=json, status_code=resp.status)
            except Exception as e:
                response=JSONResponse(content=json, status_code=500)
        res= get_response_header_data(response.raw_headers)
        if req['bearer_token'] is not None: 
            async with sessionMaker() as session: 
                await process_user(session=session,user_id=req['user_id'])
                await process_token(session=session,bearer_token=req['bearer_token'],status=response.status_code,response_length=res['response_length'],first_ip=req['origin'],user_id=req['user_id'])  #zpracovává JWT na základě odpovědí
        data_exporter(request_duration=request_duration,respone_length=res['response_length'],success=True,method='POST',origin=req['origin'],media_type=res['mime_type'],referer=req['referer'])
        if( response.status_code!=200):
            request_log(bearer_token=req['bearer_token'],ip_address=req['origin'],status_code=response.status_code)
            return JSONResponse(content=json,status_code=418 if str(status_block)=='True' else response.status_code)
        return response
    else: 
        request_log(bearer_token=req['bearer_token'],ip_address=req['origin'],status_code=status_code[0])
        response=JSONResponse(content=None,status_code=418 if str(status_block)=='True' else status_code[0])
        server_authentication_rejected_total.inc()
        return response

@app.get('/metric')
async def get_metrics():
    return Response(
        content= generate_latest(),
        media_type='text/plain')


