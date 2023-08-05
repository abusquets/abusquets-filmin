from typing import Optional, Type, Union

from pydantic import UUID4, BaseModel, Extra, Field, validator


class CreateProductionCompanyResponseDTO(BaseModel):
    uuid: UUID4


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
