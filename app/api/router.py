from fastapi import APIRouter

from app.api.v1.routes.link_routes import router as links_routes

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(links_routes)
