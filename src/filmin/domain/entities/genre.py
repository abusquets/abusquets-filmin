from dataclasses import dataclass

from filmin.domain.entities.value_objects import GenreId


@dataclass(kw_only=True)
class Genre:
    code: GenreId
    name: str
