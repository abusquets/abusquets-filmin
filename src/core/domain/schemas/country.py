from dataclasses import dataclass


@dataclass(kw_only=True)
class BaseCountry:
    name: str


@dataclass(kw_only=True)
class Country(BaseCountry):
    code: str
