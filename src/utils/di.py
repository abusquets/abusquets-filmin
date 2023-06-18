from typing import Any, Callable, Dict


class DIContainer:
    _register: Dict[str, Callable[..., Any]]

    def __init__(self) -> None:
        self._register = {}

    def __getattribute__(self, name: str) -> Any:
        ret = None
        if name == '_register' or name.startswith('__'):
            return super().__getattribute__(name)

        if name not in self._register:
            f = super().__getattribute__(f'_get_{name}')
            ret = f()
            if getattr(f, 'singleton', False):
                self._register[name] = ret
            return ret
        else:
            return self._register[name]
