from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
import uuid as uuid_lib

from filmin.domain.schemas.genre import Genre
from filmin.domain.schemas.movie_collection import MovieCollection


@dataclass(kw_only=True)
class BaseMovie:
    title: str
    release_date: Optional[date] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    popularity: Optional[float] = None
    runtime: Optional[int] = None
    collection: Optional[MovieCollection] = None
    overview: Optional[str] = None
    genres: List[Genre] = field(default_factory=list)
    original_language: Optional[str] = None


@dataclass(kw_only=True)
class Movie(BaseMovie):
    uuid: uuid_lib.UUID = field(default_factory=uuid_lib.uuid4)
