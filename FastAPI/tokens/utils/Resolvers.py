import uuid
from sqlalchemy import select
from functools import cache

from tokens.DBModel.DBToken import Token
from tokens.DBModel.DBUser import User
from tokens.DBModel.DBViolation import Violation
def update(destination, source=None, extraValues={}):
    if source is not None:
        for name in dir(source):
            print("names:",name)
            if name.startswith("_"):
                continue
            value = getattr(source, name)
            if value is not None:
                setattr(destination, name, value)
    for name, value in extraValues.items():
        setattr(destination, name, value)

    return destination
def createLoader(asyncSessionMaker, DBModel):
    baseStatement = select(DBModel)
    class Loader:
        async def load(self, id):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(id=id)
                rows = await session.execute(statement)
                rows = rows.scalars()
                row = next(rows, None)
                return row
        
        async def filter_by(self, **kwargs):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(**kwargs)
                rows = await session.execute(statement)
                rows = rows.scalars()
                row = next(rows, None)
                print('row by tokens',row)
                return row
        async def filter_by_list(self, **kwargs):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(**kwargs)
                rows=await session.execute(statement)
                rows=rows.scalars()
                return rows
        async def get_all(self):
            async with asyncSessionMaker() as session:
                rows=await session.execute(baseStatement)
                rows=rows.scalars()
                return rows
        async def insert(self, entity, extra={}):
            newdbrow = DBModel()
            print('insert is called here')
            update(newdbrow,entity,extra)
            print('new dbrow',newdbrow)
            async with asyncSessionMaker() as session:
                session.add(newdbrow)
                await session.commit()
            return newdbrow
        async def update(self, entity, extraValues={}):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(bearer_token=entity.bearer_token)
                rows = await session.execute(statement)
                rows = rows.scalars()
                rowToUpdate = next(rows, None)
                if rowToUpdate is None:
                    return None
                rowToUpdate = update(rowToUpdate, entity, extraValues=extraValues)
                await session.commit()
                result = rowToUpdate               
            return result
        async def updatebyID (self, entity, extraValues={}):
            async with asyncSessionMaker() as session:
                statement = baseStatement.filter_by(id=entity.id)
                rows = await session.execute(statement)
                rows = rows.scalars()
                rowToUpdate = next(rows, None)
                if rowToUpdate is None:
                    return None
                rowToUpdate = update(rowToUpdate, entity, extraValues=extraValues)
                await session.commit()
                result = rowToUpdate               
            return result
    return Loader()
def createLoaders(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def tokens(self):
            return createLoader(asyncSessionMaker, Token)
        @property
        @cache
        def users(self):
            return createLoader(asyncSessionMaker,User)
        @property
        @cache
        def violations(self):
            return createLoader(asyncSessionMaker,Violation)
    return Loaders()
def createLoadersContext(asyncSessionMaker):
    return {"loaders": createLoaders(asyncSessionMaker)}
def getLoadersFromInfo(info):
    return info.context["loaders"]
