from dataclasses import dataclass, field
import uuid as uuid_lib


@dataclass(kw_only=True)
class BaseMovieCollection:
    name: str


@dataclass(kw_only=True)
class MovieCollection(BaseMovieCollection):
    uuid: uuid_lib.UUID = field(default_factory=uuid_lib.uuid4)
