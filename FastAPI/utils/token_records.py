from sqlalchemy.orm import DeclarativeBase,relationship
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String ,Boolean , Integer,DateTime,select,ForeignKey
import uuid
import time
import datetime
import utils.variables
class BaseModel(DeclarativeBase):
    pass
class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    bearer_token = Column(String, comment="Authentication bearer token")
    valid = Column(Boolean,comment = 'Only valid token are allowed futher into the database', default=True)
    number_of_request = Column(Integer,comment='Number of request sent to the server in this session',default=0)
    number_of_fail_request = Column(Integer, comment = 'Number of fail request',default=0)
    response_length = Column(Integer,comment = 'Average length of a response in this session',default=0)
    first_ip=Column(String, comment = 'The first IP address that use this token when recorded',server_default='0.0.0.0')
    first_time=Column(DateTime, comment='The time of which is token is recorded into the database')
    user_id = Column(Uuid)

    #user= relationship('User',back_populates="used_token")
def update(destination, source=None, extraValues={}):
        if source is not None:
            for name in dir(source):
                if name.startswith("_"):
                    continue
                value = getattr(source, name)
                if value is not None:
                    setattr(destination, name, value)
        for name, value in extraValues.items():
            setattr(destination, name, value)
        return destination
async def get_token(session,search_str):
     async with session:
        statement = select(Token).filter_by(bearer_token=search_str)
        rows = await session.execute(statement)
        rows = rows.scalars()
        row = next(rows, None)
        return row
async def insert(session, bearer_token,first_ip,user_id):
    newdbrow = Token()
    entity={"bearer_token":bearer_token,'id':uuid.uuid1(),'valid':True,'first_time':datetime.datetime.now(),'first_ip':first_ip,'user_id':user_id}
    #když nový JWT je přidán, všechny další atributy jsou 0 
    for key, value in entity.items():
        setattr(newdbrow,key,value)
    async with session.begin():
        statement = select(Token).filter_by(bearer_token=bearer_token)
        rows = await session.execute(statement)
        rows = rows.scalars()
        row = next(rows, None)
        if row is None:
            session.add(newdbrow)
async def response_length_change(session,bearer_token,added_length):
    async with session:
        statement=select(Token).filter_by(bearer_token=bearer_token)
        rows=await session.execute(statement)
        rows=rows.scalars()
        rowToUpdate=next(rows,None)
        entity=rowToUpdate
        entity.response_length=(rowToUpdate.response_length*(rowToUpdate.number_of_request-1)+added_length)/(rowToUpdate.number_of_request) 
        #pruměrné délka za jeden dotaz (včetně chybních dotazů)
        rowToUpdate = update(rowToUpdate, entity)
        await session.commit()
async def token_update(session,update_function,search_str):
    async with session:
        statement=select(Token).filter_by(bearer_token=search_str)
        rows=await session.execute(statement)
        rows=rows.scalars()
        rowToUpdate=next(rows,None)
        entity=update_function(rowToUpdate) #změnit atributy
        rowToUpdate = update(rowToUpdate, entity)
        await session.commit()
def request_count_increase(rowToUpdate):
    entity=rowToUpdate
    entity.number_of_request=rowToUpdate.number_of_request+1
    return entity
def fail_request_count_increase(rowToUpdate):
    entity=rowToUpdate
    entity.number_of_fail_request=rowToUpdate.number_of_fail_request+1
    return entity
async def process_token(session,bearer_token,status,response_length,first_ip,user_id):
    str_error=True
    limit=0
    while str_error==True and limit<10: #skouší změnit data v databáze o 10 pokusů
        try:
            await insert(session=session,bearer_token=bearer_token,first_ip=first_ip,user_id=user_id)
            await token_update(session=session,update_function=request_count_increase,search_str=bearer_token)
        except Exception as e:
            str_error=True
            time.sleep(0.1) #čekání a pak znovu zkuší 
            limit=limit+1
        else:
            str_error = False
    str_error2=True
    while str_error2==True and limit<10:
        try:
            limit=limit+1
            if status!=200: #selhání rozumíme dotaz s kód !=200
                await token_update(session=session,update_function=fail_request_count_increase,search_str=bearer_token)
            else :
                await response_length_change(session=session,bearer_token=bearer_token,added_length=response_length)
            
        except Exception as e:
            str_error2=True
            time.sleep(0.1)
        else:
            str_error2 = False
async def check_token_validity(session,bearer_token,ip_address,status_code):
    async with session:
        pom=await get_token(session=session,search_str=bearer_token)
        if pom :
            #JWT přichazel s jiné IP adresu nemůže dále postupovat
            if pom.first_ip!=ip_address and not str(utils.variables.allow_vpn)=='True':
                status_code[0]=429 #překrotí limit vysílaní dotazů
                return False
            #JWT má živostnost uvedeno v variable.js
            time_diffirence=datetime.datetime.now()-pom.first_time
            if time_diffirence.total_seconds() > int(utils.variables.token_life_limit):
                status_code[0]=401 #neauthorizační přístup => JWT prošel živostnost
                return False
        return True

           

            