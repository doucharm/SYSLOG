
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime ,Boolean , Integer,ForeignKey
from . import BaseModel
from sqlalchemy.orm import relationship
import datetime
import uuid

class Violation(BaseModel):
    __tablename__ = "violations"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    user_id = Column(ForeignKey("users.id"),index=True)
    access_time=Column(DateTime,comment='When was this user attempted to access this content',default=datetime.datetime.now())
    requested_content=Column(String,comment='Which query was requested')
    server_response=Column(String,comment='Server response to this request',default="")
    
