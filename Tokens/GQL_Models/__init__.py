import strawberry

@strawberry.type(description="""Type for query root""")
class Query:
    from .TokenModel import token_info
    GetToken=token_info

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from TokenModel import token_insert,token_update
    InsertToken=token_insert
    TokenUpdate=token_update
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation
)