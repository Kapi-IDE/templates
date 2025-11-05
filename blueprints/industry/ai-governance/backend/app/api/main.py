from fastapi import APIRouter

from app.api.routes import governance

api_router = APIRouter()

# Include governance routes
api_router.include_router(
    governance.router,
    prefix="/governance",
    tags=["governance"]
)
