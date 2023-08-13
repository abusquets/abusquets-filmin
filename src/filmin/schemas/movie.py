from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, Field


class CreateMovieInDTO(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    release_date: Optional[date] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    collection_id: Optional[UUID] = Field(None, alias='collection')
    overview: Optional[str] = Field(None, max_length=1024)
    genres: List[str] = Field(default_factory=list)
    original_language: Optional[str] = None

    class Config:
        populate_by_name = True
        extra = Extra.forbid


class UpdateMovieInDTO(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    release_date: Optional[date] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    collection_id: Optional[UUID] = Field(None, alias='collection')
    overview: Optional[str] = Field(None, max_length=1024)
    genres: List[str] = Field(default_factory=list)
    original_language: Optional[str] = None

    class Config:
        populate_by_name = True
        extra = Extra.forbid


class UpdatePartialMovieInDTO(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    release_date: Optional[date] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    collection_id: Optional[UUID] = Field(None, alias='collection')
    overview: Optional[str] = Field(None, max_length=1024)
    genres: List[str] = Field(default_factory=list)
    original_language: Optional[str] = None

    class Config:
        populate_by_name = True
        extra = Extra.forbid
