from typing import Optional

from pydantic import BaseModel, Field


class CreateGenreInDTO(BaseModel):
    code: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)


class UpdateGenreInDTO(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class UpdatePartialGenreInDTO(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
