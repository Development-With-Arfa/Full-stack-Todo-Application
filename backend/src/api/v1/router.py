from fastapi import APIRouter
from .endpoints import tasks

# Main API router for v1
api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])