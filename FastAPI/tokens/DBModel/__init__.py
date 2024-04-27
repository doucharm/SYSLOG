from sqlalchemy.orm import DeclarativeBase
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
class BaseModel(DeclarativeBase):
    pass
async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    asyncEngine = create_async_engine(connectionstring,isolation_level="SERIALIZABLE") #queries are queued in serial order to prevent concurrent updates
    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all )
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None
    async_sessionMaker = sessionmaker(asyncEngine, expire_on_commit=False, class_=AsyncSession)
    return async_sessionMaker

import os
def ComposeConnectionString():
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "postgres")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5433")

    driver = "postgresql+asyncpg" 
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    return connectionstring
