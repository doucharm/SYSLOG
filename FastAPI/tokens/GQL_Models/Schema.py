import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .TokenModel import token_by_id,token_by_str,token_list
    GetTokenByID=token_by_id
    GetAllToken=token_list
    GetTokenByStr=token_by_str

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .TokenModel import token_insert,token_update
    TokenInsert=token_insert
    TokenUpdate=token_update
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)