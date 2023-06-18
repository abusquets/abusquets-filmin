from typing import Callable, List

from .user import create_admin


commands: List[Callable[..., None]] = [create_admin]
