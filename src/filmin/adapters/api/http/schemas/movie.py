from datetime import date
from typing import List, Optional
import uuid as _uuid

from pydantic import BaseModel, Extra, field_validator

from filmin.schemas.movie import CreateMovieInDTO, UpdateMovieInDTO, UpdatePartialMovieInDTO
from shared.api.schemas.page import PagedResponseSchema


class Genre(BaseModel):
    code: str
    name: str


class MovieCollection(BaseModel):
    uuid: str
    name: str

    @field_validator('uuid', mode='before')
    @classmethod
    def fix_uuid(cls, v: _uuid.UUID) -> str:
        return str(v)


class MovieResponse(BaseModel):
    uuid: str
    title: str
    release_date: Optional[date] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    popularity: Optional[float] = None
    runtime: Optional[int] = None
    collection: Optional[MovieCollection] = None
    overview: Optional[str] = None
    genres: List[Genre] = []
    original_language: Optional[str] = None

    @field_validator('uuid', mode='before')
    @classmethod
    def fix_uuid(cls, v: _uuid.UUID) -> str:
        return str(v)


class MovieListPagedResponse(PagedResponseSchema[MovieResponse]):
    pass


class CreateMovieRequestDTO(CreateMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False


class CreateMovieResponseDTO(BaseModel):
    uuid: str


class UpdateMovieRequestDTO(UpdateMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False


class UpdatePartialMovieRequestDTO(UpdatePartialMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False
