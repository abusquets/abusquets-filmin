from pydantic import UUID4, BaseModel, Extra

from filmin.schemas.movie import CreateMovieInDTO, UpdateMovieInDTO, UpdatePartialMovieInDTO


class CreateMovieRequestDTO(CreateMovieInDTO):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = False


class CreateMovieResponseDTO(BaseModel):
    uuid: UUID4


class UpdateMovieRequestDTO(UpdateMovieInDTO):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = False


class UpdatePartialMovieRequestDTO(UpdatePartialMovieInDTO):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = False
