import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .TokenModel import token_by_id,token_by_str,token_list
    GetTokenByID=token_by_id
    GetAllToken=token_list
    GetTokenByStr=token_by_str
    from .UserModel import user_by_id,user_list
    GetUserByID=user_by_id
    GetAllUser=user_list
    from .ViolationModel import violation_by_id,violation_by_user,violation_list
    GetViolationByID=violation_by_id
    GetViolationByUser=violation_by_user
    GetAllViolation=violation_list
    from .RougeAccessModel import rougeaccess_by_id,rougeaccess_list
    GetRougeAccessByID=rougeaccess_by_id
    GetAllRougeAccess=rougeaccess_list

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .TokenModel import token_insert,token_update
    TokenInsert=token_insert
    TokenUpdate=token_update
    from .UserModel import user_insert,user_update
    UserInsert=user_insert
    UserUpdate=user_update
    from .ViolationModel import violation_insert
    ViolationInsert=violation_insert
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)