import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .UserModel import user_by_id,user_list
    GetUserByID=user_by_id
    GetAllUser=user_list
    from .TokenModel import token_by_id,token_by_str,token_list
    GetTokenByID=token_by_id
    GetAllToken=token_list
    GetTokenByStr=token_by_str
   
    from .RougeAccessModel import rougeaccess_by_id,rougeaccess_list
    GetRougeAccessByID=rougeaccess_by_id
    GetAllRougeAccess=rougeaccess_list

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .UserModel import user_insert,user_update
    UserInsert=user_insert
    UserUpdate=user_update
    from .TokenModel import token_insert,token_update
    TokenInsert=token_insert
    TokenUpdate=token_update
 
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)