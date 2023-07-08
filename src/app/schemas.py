from typing import Optional

from pydantic import BaseModel


class Profile(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    is_admin: bool


class Session(BaseModel):
    username: str
    profile: Profile
