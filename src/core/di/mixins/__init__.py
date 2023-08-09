from .country import CountryContainerMixin
from core.di.mixins.user import UserContainerMixin


class CoreContainerMixin(CountryContainerMixin, UserContainerMixin):
    pass
