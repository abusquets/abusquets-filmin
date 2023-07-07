import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from filmin.api.router import router as filmin_router

from app.setup_logging import setup_logging
from core.api.router import router as core_router
from shared.exceptions import APPException


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(core_router)
app.include_router(filmin_router)


@app.exception_handler(APPException)
async def custom_exception_handler(request: Request, exc: APPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': {'code': exc.code, 'message': exc.message}},
    )


@app.get('/')
async def root() -> dict:
    return {'message': 'Hello World'}
