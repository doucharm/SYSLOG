from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime
from . import BaseModel
import uuid

class RougeAccess(BaseModel):
    __tablename__ = "rougeaccess"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    bearer_token = Column(String, comment="Authentication bearer token")
    access_ip = Column(String, comment = 'The IP address that use a JWT of another address')
    true_ip = Column(String, comment = 'The IP address that own the token')
    access_time = Column(DateTime, comment='The time of access')
