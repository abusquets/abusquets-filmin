from dataclasses import dataclass


@dataclass(kw_only=True)
class Genre:
    code: str
    name: str
