from dataclasses import dataclass, field
import uuid as uuid_lib


@dataclass(kw_only=True)
class BaseProductionCompany:
    name: str


@dataclass(kw_only=True)
class ProductionCompany(BaseProductionCompany):
    uuid: uuid_lib.UUID = field(default_factory=uuid_lib.uuid4)
