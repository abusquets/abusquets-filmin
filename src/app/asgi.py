from contextlib import asynccontextmanager
import logging

from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from filmin.api.router import router as filmin_router

from .app_container import AppContainer
from app.setup_logging import setup_logging
from auth.adapters.api.http.router import router as auth_router
from config import settings
from core.adapters.api.http.router import router as core_router
from shared.exceptions import APPException


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    await AppContainer().cache_repository.init()
    # Start redis connection pool
    yield
    # Stop redis connection pool
    await AppContainer().cache_repository.close()


app = FastAPI(debug=settings.DEBUG, openapi_url=None, lifespan=lifespan)


@app.get('/')
async def root() -> dict:
    return {'message': 'Hello World'}


api_app = FastAPI(title=settings.PROJECT_NAME, description=settings.PROJECT_DESCRIPTION, version=settings.VERSION)

api_app.include_router(auth_router)
api_app.include_router(core_router)
api_app.include_router(filmin_router)

app.mount('/api/v1', api_app)


@api_app.exception_handler(APPException)
async def custom_exception_handler(request: Request, exc: APPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': {'code': exc.code, 'message': exc.message}},
    )
