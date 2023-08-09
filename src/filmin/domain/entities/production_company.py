from dataclasses import dataclass, field
import uuid as uuid_lib

from filmin.domain.entities.value_objects import ProductionCompanyId


@dataclass(kw_only=True)
class BaseProductionCompany:
    name: str


@dataclass(kw_only=True)
class ProductionCompany(BaseProductionCompany):
    uuid: ProductionCompanyId = field(default_factory=uuid_lib.uuid4)
