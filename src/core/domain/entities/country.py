from dataclasses import dataclass

from core.domain.entities.value_objects import CountryId


@dataclass(kw_only=True)
class BaseCountry:
    name: str


@dataclass(kw_only=True)
class Country(BaseCountry):
    code: CountryId
