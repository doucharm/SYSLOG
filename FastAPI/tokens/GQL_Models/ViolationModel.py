import uuid
import strawberry
import datetime
import typing
from tokens.utils.Resolvers import getLoadersFromInfo
from .GraphPermisson import OnlyForAuthentized

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserModel")]


@strawberry.federation.type(keys=["id"],description="""Entity representing an attempt to access content above permission level """,)
class ViolationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id:uuid.UUID):
        if id is None: 
            return None
        loaders = getLoadersFromInfo(info)
        result = await loaders.violations.load(id=id)
        return result
    @strawberry.field(description="""Primary key""")
    def id(self) -> uuid.UUID:
        return self.id
    @strawberry.field(description="""The time when this violation happen""")
    def access_time(self) -> typing.Optional[datetime.datetime]:
        return self.access_time
    @strawberry.field(description="""The user that caused this violation""")
    def user_id(self) -> typing.Optional[uuid.UUID]:
        return self.user_id
    @strawberry.field(description="""The query requested that caused a violation""")
    def requested_content(self) -> typing.Optional[str]:
        return self.requested_content    
    @strawberry.field(description="""Server's response to this violation""")
    def server_response(self) -> typing.Optional[str]:
        return self.server_response
    async def user(self, info: strawberry.types.Info) -> typing.Optional["UserGQLModel"]:
        loader = getLoadersFromInfo(info).users
        result = await loader.filter_by(user_id=self.id)
        return result
    
#################################################################
##____________________Query session____________________________##
#################################################################
@strawberry.field(description="""Return information about a violation when search by id""",permission_classes=[OnlyForAuthentized(isList=False)])
async def violation_by_id(info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ViolationGQLModel]:
    return await ViolationGQLModel.resolve_reference(info, id)
@strawberry.field(description="""Return all violation of GDPR from one user""",permission_classes=[OnlyForAuthentized(isList=False)])
async def violation_by_user(info: strawberry.types.Info,id_user:uuid.UUID) -> typing.List[ViolationGQLModel]:
    loaders = getLoadersFromInfo(info).violations
    return await loaders.filter_by_list(user_id = id_user)
@strawberry.field(description="""Return all violations in the database""",permission_classes=[OnlyForAuthentized(isList=True)])
async def violation_list(info:strawberry.types.Info) -> typing.List[ViolationGQLModel]:
    loaders=getLoadersFromInfo(info).violations
    result = await loaders.get_all()
    return result
    
###################################################################
##_____________________________Mutations_________________________##
###################################################################

@strawberry.input(description="A violation is recorded")
class ViolationInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated",default=None)
    user_id: uuid.UUID = strawberry.field(description='The identification of the client that cause this violation')
    access_time:typing.Optional[datetime.datetime]=strawberry.field(description='When was this violation caused',default=None)
    requested_content:typing.Optional[str]=strawberry.field(description='Requested query outside of clearance level',default='')
    server_response:typing.Optional[str]=strawberry.field(description='Response from server',default='')
@strawberry.type(description="result of CUD operation on token")
class ViolationResultGQLModel:
    id: typing.Optional[uuid.UUID] = None
    msg: str = strawberry.field(description="result of the operation ok / fail", default="")

    @strawberry.field(description="""returns the violation""")
    async def violation(self, info: strawberry.types.Info) -> ViolationGQLModel:
        if self.id is not None:
            return await ViolationGQLModel.resolve_reference(info, self.id)

@strawberry.mutation(description="Write new violation into database")
async def violation_insert(self, info: strawberry.types.Info, violation: ViolationInsertGQLModel) -> ViolationResultGQLModel:
    if  violation.id is None:
        violation.id=uuid.uuid1()
    if not violation.access_time:
        violation.access_time=datetime.datetime.now()
    print(violation)
    loader = getLoadersFromInfo(info).violations
    row = await loader.insert(violation)
    result = ViolationResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result
