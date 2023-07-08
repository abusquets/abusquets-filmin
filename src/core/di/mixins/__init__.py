from .country import CountryRepositoryContainerMixin
from .user import UserServiceContainerMixin


class CoreContainerMixin(CountryRepositoryContainerMixin, UserServiceContainerMixin):
    pass
