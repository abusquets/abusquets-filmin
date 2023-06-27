from filmin.di.mixins.genre import GenreContainerMixin
from filmin.di.mixins.movie import MovieContainerMixin
from filmin.di.mixins.production_company import ProductionCompanyContainerMixin


class FilminContainerMixin(ProductionCompanyContainerMixin, GenreContainerMixin, MovieContainerMixin):
    pass
