from .country import CountryContainerMixin
from .user import UserServiceContainerMixin


class CoreContainerMixin(CountryContainerMixin, UserServiceContainerMixin):
    pass
