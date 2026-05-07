from fastapi import APIRouter

from app.api.v1 import meetings, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="")

