from pydantic import BaseModel, Extra

from filmin.schemas.genre import CreateGenreInDTO, UpdateGenreInDTO, UpdatePartialGenreInDTO


class CreateGenreRequestDTO(CreateGenreInDTO):
    class Config:
        extra = Extra.forbid


class CreateGenreResponseDTO(BaseModel):
    code: str


class UpdateGenreRequestDTO(UpdateGenreInDTO):
    class Config:
        extra = Extra.forbid


class UpdatePartialGenreRequestDTO(UpdatePartialGenreInDTO):
    class Config:
        extra = Extra.forbid
