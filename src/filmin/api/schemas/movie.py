from pydantic import UUID4, BaseModel, Extra

from filmin.schemas.movie import CreateMovieInDTO, UpdateMovieInDTO, UpdatePartialMovieInDTO


class CreateMovieRequestDTO(CreateMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False


class CreateMovieResponseDTO(BaseModel):
    uuid: UUID4


class UpdateMovieRequestDTO(UpdateMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False


class UpdatePartialMovieRequestDTO(UpdatePartialMovieInDTO):
    class Config:
        extra = Extra.forbid
        populate_by_name = False
