import uuid
import strawberry
import typing
from tokens.utils.Resolvers import getLoadersFromInfo
import datetime
TokenGQLModel = typing.Annotated["TokenGQLModel", strawberry.lazy(".TokenModel")]

@strawberry.federation.type(keys=["id"],description="""Entity representing a recorded rouge access """,)
class RougeAccessGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id:uuid.UUID):
        if id is None: 
            return None
        loaders = getLoadersFromInfo(info)
        result = await loaders.rougeaccess.load(id=id)
        return result

    @strawberry.field(description="""Identificator""")
    def id(self) -> uuid.UUID:
        return self.id
    @strawberry.field(description="""The bearer token which was used""")
    def bearer_token(self) -> typing.Optional[str]:
        return self.bearer_token
    @strawberry.field(description="""The IP address that use another client's JWT""")
    def access_ip(self) -> str:
        return self.access_ip

    @strawberry.field(description="""The original IP address of the JWT""")
    def true_ip(self) -> typing.Optional[str]:
        return self.true_ip
    @strawberry.field(description="""The time when this access  was recorded""")
    def access_time(self) -> typing.Optional[datetime.datetime]:
        return self.access_time
# #################################################################
# ##____________________Query session____________________________##
# #################################################################
@strawberry.field(description="""Return information about an attempt to access with a possible frauduent JWT""")
async def rougeaccess_by_id(info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[RougeAccessGQLModel]:
    return await RougeAccessGQLModel.resolve_reference(info, id)
@strawberry.field(description="""Return all the fraudulent access in the database""")
async def rougeaccess_list(info:strawberry.types.Info) -> typing.List[RougeAccessGQLModel]:
    loaders=getLoadersFromInfo(info).rougeaccess
    result = await loaders.get_all()
    return result
    
# ###################################################################
# ##_____________________________Mutations_________________________##
# ###################################################################

