import logging
from sqlalchemy.future import select
import strawberry

import os

from functools import cache
import aiohttp

@cache
def OnlyForAuthentized(isList=False):
    class OnlyForAuthentized(strawberry.permission.BasePermission):
        message = "User is not authenticated"

        async def has_permission(
            self, source, info: strawberry.types.Info, **kwargs
        ) -> bool:
            
            
            #user = getUserFromInfo(info)
            #return (False if user is None else True)
            return True
        
        def on_unauthorized(self):
            return ([] if isList else None)

            
            
    return OnlyForAuthentized
