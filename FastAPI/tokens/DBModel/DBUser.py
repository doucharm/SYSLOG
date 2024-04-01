from sqlalchemy.schema import Column
from sqlalchemy import Uuid,Boolean , Integer
from sqlalchemy.orm import relationship
from . import BaseModel
import uuid
class User(BaseModel):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1())
    valid = Column(Boolean,comment = 'Valid user', default=True)
    number_of_request = Column(Integer,comment='Number of request sent to the server by this user',default=0)
    number_of_fail_request = Column(Integer, comment = 'Number of fail request made by this user',default=0)
    response_length = Column(Integer,comment = 'Average length of a response for a request made by this user',default=0)
    number_of_unauthorized_request=Column(Integer,comment='Number of request that is rejected due to having no permission',default=0)

    used_token = relationship('Token',back_populates='user')
    
