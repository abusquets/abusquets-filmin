from typing import Optional, Type, Union
import uuid as _uuid

from pydantic import BaseModel, Extra, Field, field_validator, validator

from shared.api.schemas.page import PagedResponseSchema


class ProductionCompanyResponse(BaseModel):
    uuid: str
    name: str

    @field_validator('uuid', mode='before')
    @classmethod
    def fix_uuid(cls, v: _uuid.UUID) -> str:
        return str(v)


class ProductionCompanyListPagedResponse(PagedResponseSchema[ProductionCompanyResponse]):
    pass


class CreateProductionCompanyResponseDTO(BaseModel):
    uuid: str


class CreateProductionCompanyRequestDTO(BaseModel):
    name: str = Field(min_length=1, max_length=255)

    class Config:
        extra = Extra.forbid


class UpdateProductionCompanyRequestDTO(BaseModel):
    name: str = Field(min_length=1, max_length=255)

    class Config:
        extra = Extra.forbid


class UpdatePartialProductionCompanyRequestDTO(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=255)

    @validator('name', pre=True)
    @classmethod
    def validate_null(
        cls: Type['UpdatePartialProductionCompanyRequestDTO'], v: Union[None, str, bool]
    ) -> Union[str, bool]:
        if v is None:
            raise ValueError('Null is not allowed')
        return v

    class Config:
        extra = Extra.forbid
