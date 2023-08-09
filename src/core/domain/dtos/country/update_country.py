from typing import Optional

from pydantic import BaseModel, Field


class UpdatePartialCountryInDTO(BaseModel):
    name: Optional[str] = Field(max_length=255)
