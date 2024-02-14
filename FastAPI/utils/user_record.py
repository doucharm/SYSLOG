from sqlalchemy.schema import Column
from sqlalchemy import Uuid,Boolean ,select
from sqlalchemy.orm import relationship,DeclarativeBase
import uuid

import time
class BaseModel(DeclarativeBase):
    pass
class User(BaseModel):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    valid = Column(Boolean,comment = 'Valid user', default=True)
    #used_token = relationship('Token',back_populates='user')
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
async def add_user(session,user_id):#zjiští existenci uživatele v databázi a pokud není tak přidáme mu 
    async with session.begin():
        statement=select(User).filter_by(id=user_id)
        rows =await session.execute (statement)
        rows=rows.scalars()
        row=next(rows,None)
        if row is None:
            new_row=User()
            new_user={'id':user_id,'valid':True}
            for key, value in new_user.items():
                setattr(new_row,key,value)
            print(new_row.id)
            session.add(new_row)
async def process_user(session,user_id):
    updated=False
    i=0
    while not updated and i <10: #ozmezit počet pokusů do 10
        try:
            await add_user(session,user_id)
        except Exception as e:
            updated=False
            print(e)
            time.sleep(0.1)
            i=i+1
        else:
            updated=True
                   

        


    
        
        


