import uuid
import strawberry
import typing
from tokens.utils.Resolvers import getLoadersFromInfo
from .GraphPermisson import OnlyForAuthentized

TokenGQLModel = typing.Annotated["TokenGQLModel", strawberry.lazy(".TokenModel")]

@strawberry.federation.type(keys=["id"],description="""Entity representing a client """,)
class UserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id:uuid.UUID):
        if id is None: 
            return None
        loaders = getLoadersFromInfo(info)
        result = await loaders.users.load(id=id)
        return result

    @strawberry.field(description="""A client identificator""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""Validity of a client""")
    def valid(self) -> typing.Optional[bool]:
        return self.valid

    @strawberry.field(description="""Number of requests that the user has made""")
    def number_of_request(self) -> typing.Optional[int]:
        return self.number_of_request

    @strawberry.field(description="""Number of request with a fail response message""")
    def number_of_fail_request(self) -> typing.Optional[int]:
        return self.number_of_fail_request

    @strawberry.field(description="""Average length of the responses for requests made by this user""")
    def response_length(self) -> typing.Optional[int]:
        return self.response_length
    
    @strawberry.field(description="""Number of request with a fail response message of 401""")
    def number_of_unauthorized_request(self) -> typing.Optional[int]:
        return self.number_of_unauthorized_request
    @strawberry.field(description="""List of JWT requested by this user""",)
    async def used_token(self, info: strawberry.types.Info) -> typing.List["TokenGQLModel"]:
        loader = getLoadersFromInfo(info).tokens
        result = await loader.filter_by_list(user_id=self.id)
        return result
# #################################################################
# ##____________________Query session____________________________##
# #################################################################
@strawberry.field(description="""Return information about a client when search by id""",permission_classes=[OnlyForAuthentized(isList=False)])
async def user_by_id(info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[UserGQLModel]:
    return await UserGQLModel.resolve_reference(info, id)
@strawberry.field(description="""Return all users in the database""",permission_classes=[OnlyForAuthentized(isList=True)])
async def user_list(info:strawberry.types.Info) -> typing.List[UserGQLModel]:
    loaders=getLoadersFromInfo(info).users
    result = await loaders.get_all()
    return result
    
# ###################################################################
# ##_____________________________Mutations_________________________##
# ###################################################################

@strawberry.input(description="Create a client")
class UserInsertGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID) of the client ")
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used",default=True)
    number_of_request: typing.Optional[int] = strawberry.field(description="Number of request carried out by this token/client session",default=0)
    number_of_fail_request: typing.Optional[int] = strawberry.field(description="Number of fail response message for request carried out by this token/client session",default=0)
    response_length: typing.Optional[int] = strawberry.field(description="Average length for successful response",default=0)
    number_of_unauthorized_request: typing.Optional[int] = strawberry.field(description="Average length for response with code 401",default=0)
    
@strawberry.input(description="Update the information of a client")
class UserUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID")
    valid: typing.Optional[bool] = strawberry.field(description="Only valid token can be used",default=None)
    number_of_request: typing.Optional[int] = strawberry.field(description="Number of request carried out by this token/client session",default=None)
    number_of_fail_request: typing.Optional[int] = strawberry.field(description="Number of fail response message for request carried out by this token/client session",default=None)
    response_length: typing.Optional[int] = strawberry.field(description="Average length for successful response",default=None)
    number_of_unauthorized_request: typing.Optional[int] = strawberry.field(description="Number of responses with code 401",default=None)



@strawberry.type(description="result of CUD operation on user")
class UserResultGQLModel:
    id: typing.Optional[uuid.UUID] = None
    msg: str = strawberry.field(description="result of the operation ok / fail", default="")

    @strawberry.field(description="""returns the client""")
    async def user(self, info: strawberry.types.Info) -> UserGQLModel:
        if self.id is not None:
            return await UserGQLModel.resolve_reference(info, self.id)

@strawberry.mutation(description="Write new user into database")
async def user_insert(self, info: strawberry.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
    if user.id is None:
        user.id=uuid.uuid1()
    loader = getLoadersFromInfo(info).users
    row = await loader.insert(user)
    result = UserResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="Update the user in database")
async def user_update(self, info: strawberry.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
    loader = getLoadersFromInfo(info).users
    row = await loader.updatebyID(user)
    result = UserResultGQLModel()
    result.id = user.id
    if row is None:
        result.msg = "Failed "
    else:    
        result.msg = "Success"
    return result
