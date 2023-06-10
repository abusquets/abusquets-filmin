import logging

from fastapi import FastAPI

from app.setup_logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}
