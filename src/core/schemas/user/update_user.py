from typing import Optional

from pydantic import BaseModel, Field


class UpdatePartialUserInDTO(BaseModel):
    email: Optional[str] = Field(max_length=255)
    first_name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    password: Optional[str] = Field(max_length=255)
