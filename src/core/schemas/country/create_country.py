from pydantic import BaseModel, Field


class CreateCountryInDTO(BaseModel):
    code: str = Field(max_length=2)
    name: str = Field(max_length=255)
