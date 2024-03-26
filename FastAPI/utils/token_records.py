from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String ,Boolean , Integer,DateTime,select
import uuid
import time,os
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
    #new token is recognised and inserted into the database to monitor
    for key, value in entity.items():
        setattr(newdbrow,key,value)
    async with session.begin():
        statement = select(Token).filter_by(bearer_token=bearer_token)
        rows = await session.execute(statement)
        rows = rows.scalars()
        row = next(rows, None)
        if row is None:
            session.add(newdbrow)
async def token_update(session,bearer_token,status,response_length):
   async with session:
        statement=select(Token).filter_by(bearer_token=bearer_token)
        rows=await session.execute(statement)
        rows=rows.scalars()
        rowToUpdate=next(rows,None)
        rowToUpdate.number_of_request=rowToUpdate.number_of_request+1
        if status==200:
            if rowToUpdate.number_of_request==1:
                rowToUpdate.response_length=response_length
            else:
                rowToUpdate.response_length=(rowToUpdate.response_length*(rowToUpdate.number_of_request-1 - rowToUpdate.number_of_fail_request)+response_length)/rowToUpdate.number_of_request
        else:
            rowToUpdate.number_of_fail_request=rowToUpdate.number_of_fail_request+1
        await session.commit()
async def process_token(session,bearer_token,status,response_length,first_ip,user_id):
    need_retry=True
    retry_count=0
    retry_limit=int(os.environ.get('RETRY_LIMIT','10'))
    while need_retry and retry_count <= retry_limit: #Attempt to update already existing token with new information
        try:
            await insert(session=session,bearer_token=bearer_token,first_ip=first_ip,user_id=user_id)
            await token_update(session=session,bearer_token=bearer_token,status=status,response_length=response_length)
        except Exception as e:
            need_retry=True
            time.sleep(0.05)
            retry_count=retry_count+1
        else:
            need_retry = False
    if retry_count>retry_limit:
        print('Failed to update token +{bearer_token}')
async def check_token_validity(session,bearer_token,ip_address,status_code):
    async with session:
        jwt_token=await get_token(session=session,search_str=bearer_token) #check wether there is an token the database already
        if jwt_token==None:
            return True
        else:
            if not jwt_token.valid:
                return False
            #Check for IP addresses
            if jwt_token.first_ip!=ip_address and not str(utils.variables.allow_vpn)=='True':
                status_code[0]=429 #Code 429 indicate that the "source" has already sent too much request
                return False
            #JWT have a time limit which are checked 
            time_diffirence=datetime.datetime.now()-jwt_token.first_time
            if time_diffirence.total_seconds() > int(utils.variables.token_life_limit):
                status_code[0]=401 #neauthorizační přístup => JWT prošel živostnost
                return False
        return True

           

            