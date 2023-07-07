from .country import CountryRepositoryContainerMixin
from .user import UserRepositoryContainerMixin


class CoreContainerMixin(CountryRepositoryContainerMixin, UserRepositoryContainerMixin):
    pass
