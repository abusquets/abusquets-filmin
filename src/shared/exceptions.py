from typing import Any


class APPException(Exception):
    status_code = 500
    code = 'app-exception'
    message = 'An error occurred'


class NotFound(APPException):
    status_code = 404
    code: str
    message: str

    def __init__(self, entity: str, *args: Any, **kwargs: Any):
        self.code = f'{entity.lower()}-not-found'
        self.message = f'{entity} not found'
        super().__init__(*args, **kwargs)


class AlreadyExists(APPException):
    status_code = 422
    code: str
    message: str

    def __init__(self, entity: str, *args: Any, **kwargs: Any):
        self.code = f'{entity.lower()}-already-exists'
        self.message = f'{entity} already exists'
        super().__init__(*args, **kwargs)
