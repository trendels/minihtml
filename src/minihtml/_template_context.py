from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field

from ._core import Node


@dataclass
class TemplateContext:
    _styles: dict[int, Node] = field(default_factory=dict)
    _scripts: dict[int, Node] = field(default_factory=dict)

    def add_style(self, node: Node):
        self._styles[id(node)] = node

    def add_script(self, node: Node):
        self._scripts[id(node)] = node

    @property
    def styles(self) -> Iterable[Node]:
        return self._styles.values()

    @property
    def scripts(self) -> Iterable[Node]:
        return self._scripts.values()


_template_context = ContextVar[TemplateContext]("template_context")


def register_template_styles(nodes: Sequence[Node]) -> None:
    if ctx := _template_context.get(None):
        for node in nodes:
            ctx.add_style(node)


def register_template_scripts(nodes: Sequence[Node]) -> None:
    if ctx := _template_context.get(None):
        for node in nodes:
            ctx.add_script(node)


def get_template_context() -> TemplateContext:
    return _template_context.get()


@contextmanager
def template_context() -> Iterator[None]:
    token = _template_context.set(TemplateContext())
    try:
        yield
    finally:
        _template_context.reset(token)
