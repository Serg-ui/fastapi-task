from fastapi import APIRouter
from api.users import router as users_router


routers = APIRouter()
routers.include_router(users_router.router, prefix='/api/user')


