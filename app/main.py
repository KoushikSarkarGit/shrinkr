from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import Settings, settings
from app.core.dependencies import get_settings
from app.middleware.request_context import request_context_middleware
from app.api.register_exception_handlers import register_exception_handlers
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Shrinkr application starting...")

    yield

    print("Shrinkr application shutting down...")


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=request_context_middleware,
)

app.include_router(api_router)

register_exception_handlers(app)


@app.get("/healthz")
async def get_health(
    app_settings: Settings = Depends(get_settings),
):
    return {"status": "Ok", "environment": app_settings.environment}
