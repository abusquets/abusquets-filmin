from typing import Optional

from pydantic import BaseModel


class Profile(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    is_admin: bool


class Session(BaseModel):
    uuid: str
    expires: int
    username: str
    profile: Profile


class DetailResponse(BaseModel):
    detail: str
