import uuid
import strawberry
import datetime
import typing
from utils.Resolvers import getLoadersFromInfo
@strawberry.federation.type(keys=["id"],description="""Entity representing a token of a session """,)
class TokenGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id:uuid.UUID):
        if id is None: 
            return None
        loaders = getLoadersFromInfo(info)
        result = await loaders.tokens.load(id=id)
        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Bearer token for authentication""")
    def bearer_token(self) -> str:
        return self.bearer_token

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

    @strawberry.field(description="""The last time this token was changed""")
    def lastchange(self) -> datetime.datetime:
        if self.lastchange == None:
            return datetime.datetime.now()
        else :
            return self.lastchange
        
#################################################################
##____________________Query session____________________________##
#################################################################
@strawberry.field(description="""Return information about a token when search by id""")
async def token_by_id(info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[TokenGQLModel]:
    return await TokenGQLModel.resolve_reference(info, id)
@strawberry.field(description="""Return information about a token when search by token""")
async def token_by_str(info: strawberry.types.Info,search_str:str) -> typing.Optional[TokenGQLModel]:
    loaders = getLoadersFromInfo(info).tokens
    return await loaders.filter_by(bearer_token = search_str)
@strawberry.field(description="""Return all tokens in the database""")
async def token_list(info:strawberry.types.Info) -> typing.List[TokenGQLModel]:
    loaders=getLoadersFromInfo(info).tokens
    result = await loaders.get_all()
    return result
    
###################################################################
##_____________________________Mutations_________________________##
###################################################################

@strawberry.input(description="Create a token corelate to a session")
class TokenInsertGQLModel:
    bearer_token: str = strawberry.field(description="Bearer token")
    id: typing.Optional[strawberry.ID] = strawberry.field(description="primary key (UUID), could be client generated",default=None)
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used",default=True)
    number_of_request: typing.Optional[int] = strawberry.field(description="Number of request carried out by this token/client session",default=0)
    number_of_fail_request: typing.Optional[int] = strawberry.field(description="Number of fail response message for request carried out by this token/client session",default=0)
    response_length: typing.Optional[int] = strawberry.field(description="Average length for successful response",default=0)

@strawberry.input(description="Update the information of a token")
class TokenUpdateGQLModel:
    id: strawberry.ID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp / token for multiuser updates")
    bearer_token: typing.Optional[str] = strawberry.field(description="Bearer token")
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used")
    number_of_request: typing.Optional[int] = strawberry.field(description="Number of request carried out by this token/client session",default=0)
    number_of_fail_request: typing.Optional[int] = strawberry.field(description="Number of fail response message for request carried out by this token/client session",default=0)
    response_length: typing.Optional[int] = strawberry.field(description="Average length for successful response")



@strawberry.type(description="result of CUD operation on token")
class TokenResultGQLModel:
    id: typing.Optional[strawberry.ID] = None
    msg: str = strawberry.field(description="result of the operation ok / fail", default="")

    @strawberry.field(description="""returns the token""")
    async def token(self, info: strawberry.types.Info) -> TokenGQLModel:
        return await TokenGQLModel.resolve_reference(info, self.id)

@strawberry.mutation(description="Write new token into database")
async def token_insert(self, info: strawberry.types.Info, token: TokenInsertGQLModel) -> TokenResultGQLModel:
    print("this is the test",token.__dict__)
    if token.id is None:
        token.id=uuid.uuid1()
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
        result.msg = "Failed "
    else:    
        result.msg = "Success"
    return result
