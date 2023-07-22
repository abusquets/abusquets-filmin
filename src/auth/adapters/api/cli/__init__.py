from typing import Callable, List

from .secret import create_secret


commands: List[Callable[..., None]] = [create_secret]
