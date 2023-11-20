from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String ,Boolean , Integer,select
import uuid
class BaseModel(DeclarativeBase):
    pass

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    asyncEngine = create_async_engine(connectionstring)
    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

class Token(BaseModel):
    __tablename__ = "tokens"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    bearer_token = Column(String, comment="Authentication bearer token")
    valid = Column(Boolean,comment = 'Only valid token are allowed futher into the database')
    number_of_request = Column(Integer,comment='Number of request sent to the server in this session',default=0)
    number_of_fail_request = Column(Integer, comment = 'Number of fail request',default=0)
    response_length = Column(Integer,comment = 'Average length of a response in this session',default=0)

import os
def ComposeConnectionString():
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    return connectionstring

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
async def insert(session, bearer_token):
    newdbrow = Token()
    entity={"bearer_token":bearer_token,'id':uuid.uuid1()}
    for key, value in entity.items():
        setattr(newdbrow,key,value)
    async with session:
        session.add(newdbrow)
        await session.commit()
    return newdbrow
async def request_length_change(session,entity,added_length):
    async with session:
        statement=select(Token).filter_by(bearer_token=entity.bearer_token)
        rows=await session.execute(statement)
        rows=rows.scalars()
        rowToUpdate=next(rows,None)
        entity.request_length=(rowToUpdate.request_length*rowToUpdate.number_of_request+added_length)/(rowToUpdate.number_of_request+1)
        rowToUpdate = update(rowToUpdate, entity)
        await session.commit()
        result = rowToUpdate 
        return result
async def token_update(session,update_function,search_str):
    async with session:
        statement=select(Token).filter_by(bearer_token=search_str)
        rows=await session.execute(statement)
        rows=rows.scalars()
        rowToUpdate=next(rows,None)
        entity=update_function(rowToUpdate)
        rowToUpdate = update(rowToUpdate, entity)
        await session.commit()
        result = rowToUpdate 
        return result
def request_count_increase(rowToUpdate):
    entity=rowToUpdate
    entity.number_of_request=rowToUpdate.number_of_request+1
    return entity
def fail_request_count_increase(rowToUpdate):
    entity=rowToUpdate
    entity.number_of_fail_request=rowToUpdate.number_of_fail_request+1
    return entity
async def check_exist(session,bearer_token):
     if get_token(session=session,search_str=bearer_token).bearer_token is None:
         return False 
     else :
         return True
    