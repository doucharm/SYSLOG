from contextlib import asynccontextmanager
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from GQL_Models import schema
async def database_mount(app:FastAPI):
    appcontext = {}
    @asynccontextmanager
    async def initEngine(app: FastAPI):

        from DBModel import startEngine, ComposeConnectionString

        connectionstring = ComposeConnectionString()

        asyncSessionMaker = await startEngine(
            connectionstring=connectionstring,
            makeDrop=True,
            makeUp=True
        )

        appcontext["asyncSessionMaker"] = asyncSessionMaker
        yield
    app = FastAPI(lifespan=initEngine)
    @app.get('/hello')
    def hello():
        return {'hello': 'world'}


    def get_context():
        from utils.Resolvers import createLoadersContext
        return createLoadersContext(appcontext["asyncSessionMaker"])
    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context
    )
    app.include_router(graphql_app, prefix="/tokens/gql")
    return app