import sys
from contextvars import ContextVar
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


_context = ContextVar[dict[type, list[Any]]]("context")


class Context:
    def push(self) -> None:
        try:
            g = _context.get()
        except LookupError:
            g: dict[type, list[Any]] = {}
            _context.set(g)
        g.setdefault(type(self), []).append(self)

    def pop(self) -> None:
        _context.get()[type(self)].pop()

    @classmethod
    def get(cls) -> Self:
        return _context.get()[cls][-1]

    def __enter__(self) -> Self:
        self.push()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.pop()
