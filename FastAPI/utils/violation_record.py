
from sqlalchemy.schema import Column
from sqlalchemy import Uuid,String,DateTime
from sqlalchemy.orm import DeclarativeBase
import uuid
import datetime
class BaseModel(DeclarativeBase):
    pass
class Violation(BaseModel):
    __tablename__ = "violations"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    user_id = Column(Uuid)
    access_time=Column(DateTime,comment='When was this user attempted to access this content',default=datetime.datetime.now())
    requested_content=Column(String,comment='Which query was requested')
    server_response=Column(String,comment='Server response to this request',default="")
    

async def create_report(session,user_id,requested_content,server_response): #pridáme do databáze nový záznam 
    """
    Adds a new entry to the database for a user report.

    Parameters:
    - session (sqlalchemy.orm.Session): The SQLAlchemy session to interact with the database.
    - user_id (int): The ID of the user making the report.
    - requested_content (str): The content or resource requested by the user.
    - server_response (str): The response received from the server.

    Returns:
    None
    This function creates a new record in the 'Violation' table of the database, capturing information
    about a user's report. It includes details such as the user ID, requested content, server response,
    and the timestamp of the report.
    """
    async with session.begin():
        new_row=Violation()
        time=datetime.datetime.now()
        new_user={'user_id':user_id,'requested_content':requested_content,'server_response':server_response,'access_time':time}
        for key, value in new_user.items():
            setattr(new_row,key,value)
        session.add(new_row)