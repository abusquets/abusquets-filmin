from typing import Optional

from pydantic import BaseModel, Field


class CreateProductionCompanyInDTO(BaseModel):
    name: str = Field(max_length=255)


class UpdateProductionCompanyInDTO(BaseModel):
    name: str = Field(max_length=255)


class UpdatePartialProductionCompanyInDTO(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
