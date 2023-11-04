import uuid
import strawberry
import datetime
import typing
from ..Resolvers import getLoadersFromInfo
@strawberry.federation.type(keys=["id"],description="""Entity representing a token of a session """,)
class TokenGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, token: str):
        if token is None: 
            return None

        loaders = getLoadersFromInfo(info)
        eventloader = loaders.events
        result = await eventloader.load(id=id)

        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Bearer token for authentication""")
    def token(self) -> str:
        return self.token

    @strawberry.field(description="""Request with invalid token will not be allowed to access the database""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""Number of requests that the session has made""")
    def number_of_request(self) -> int:
        return self.number_of_request

    @strawberry.field(description="""Number of request with a fail response message""")
    def number_of_fail_request(self) -> int:
        return self.number_of_fail_request

    @strawberry.field(description="""Average length of the responses for requests made with this token""")
    def response_length(self) -> int:
        return self.response_length

    @strawberry.field(description="""The last time this token is changed""")
    def lastchange(self) -> datetime.datetime:
        if self.lastchange == None:
            return datetime.datetime.now()
        else :
            return self.lastchange
        
#################################################################
##____________________Query session____________________________##
#################################################################
@strawberry.field(description="""Return information about a token""")
async def token_info(info: strawberry.types.Info, token: str) -> TokenGQLModel:
    return await TokenGQLModel.resolve_reference(info, token)

###################################################################
##_____________________________Mutations_________________________##
###################################################################

@strawberry.input(description="Create a token corelate to a session")
class TokenInsertGQLModel:
    token: str = strawberry.field(description="Bearer token")
    id: typing.Optional[strawberry.ID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used",default=True)

@strawberry.input(description="Update the information of a token")
class TokenUpdateGQLModel:
    id: strawberry.ID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp / token for multiuser updates")
    token: typing.Optional[str] = strawberry.field(description="Bearer token", default=None)
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used",default=True)
    number_of_request: typing.Optional[int] = strawberry.field(description="Number of request carried out by this token/client session",default=0)
    number_of_fail_request: typing.Optional[int] = strawberry.field(description="Number of fail response message for request carried out by this token/client session",default=0)
    request_length: typing.Optional[int] = strawberry.field(description="Average length for successful response",default=0)



@strawberry.type(description="result of CUD operation on token")
class TokenResultGQLModel:
    id: typing.Optional[strawberry.ID] = None
    msg: str = strawberry.field(description="result of the operation ok / fail", default="")

    @strawberry.field(description="""returns the token""")
    async def token(self, info: strawberry.types.Info) -> TokenGQLModel:
        return await TokenGQLModel.resolve_reference(info, self.token)

@strawberry.mutation(description="write new token into database")
async def token_insert(self, info: strawberry.types.Info, token: TokenInsertGQLModel) -> TokenResultGQLModel:
    loader = getLoadersFromInfo(info).tokens
    row = await loader.insert(token)
    result = TokenResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="Update the token in database")
async def token_update(self, info: strawberry.types.Info, token: TokenUpdateGQLModel) -> TokenResultGQLModel:
    loader = getLoadersFromInfo(info).tokens
    row = await loader.update(token)
    result = TokenResultGQLModel()
    result.id = token.id
    if row is None:
        result.msg = "fail"
    else:    
        result.msg = "ok"
    return result
