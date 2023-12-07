import datetime
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime ,Boolean , Integer
from . import BaseModel
import uuid

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
