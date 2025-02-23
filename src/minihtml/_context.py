import sys
from contextvars import ContextVar
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


_context = ContextVar[dict[type, list[Any]]]("context")


class Context:
    """
    Base class for context objects.

    Implements the context manager protocol. When the context is entered, the current
    """

    def _push(self) -> None:
        try:
            g = _context.get()
        except LookupError:
            g: dict[type, list[Any]] = {}
            _context.set(g)
        g.setdefault(type(self), []).append(self)

    def _pop(self) -> None:
        _context.get()[type(self)].pop()

    def __enter__(self) -> None:
        self._push()

    def __exit__(self, *exc_info: object) -> None:
        self._pop()

    @classmethod
    def get(cls) -> Self:
        """
        Get the current instance of the context object.
        """
        return _context.get()[cls][-1]
