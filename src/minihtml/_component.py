import io
import sys
from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from typing import Callable, Concatenate, Generic, ParamSpec, TypeAlias

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from ._core import (
    ElementNonEmpty,
    HasNodes,
    Node,
    iter_nodes,
    pop_element_context,
    push_element_context,
    register_with_context,
)
from ._template_context import register_template_scripts, register_template_styles


class SlotContext:
    def __init__(self, capture: bool):
        self._capture = capture

    def __enter__(self) -> None:
        if self._capture:
            capture = ElementNonEmpty("__capture__")
            push_element_context(capture)

    def __exit__(self, *exc_info: object) -> None:
        if self._capture:
            pop_element_context()


class Slots:
    def __init__(self, slots: Sequence[str], default: str | None):
        self._slots: dict[str, list[Node | HasNodes]] = {slot: [] for slot in slots}
        self._default = default or ""
        if not slots:
            self._slots[""] = []

    def add_content(self, slot: str | None, content: list[Node | HasNodes]) -> None:
        slot = slot or self._default
        self._slots[slot].extend(content)

    def slot(self, slot: str | None = None) -> SlotContext:
        for obj in self._slots[slot or self._default]:
            register_with_context(obj)
        return SlotContext(capture=self.is_filled(slot))

    def is_filled(self, slot: str | None = None) -> bool:
        return bool(self._slots[slot or self._default])


P = ParamSpec("P")

ComponentImpl: TypeAlias = Callable[Concatenate[Slots, P], Node | HasNodes]


class Component:
    def __init__(self, callback: Callable[[Slots], Node | HasNodes], slots: Slots):
        self._callback = callback
        self._slots = slots
        self._cached_nodes: list[Node] | None = None

    def __enter__(self) -> Self:
        self._capture = ElementNonEmpty("__capture__")
        push_element_context(self._capture)
        return self

    def __exit__(self, *exc_info: object) -> None:
        parent, children = pop_element_context()
        assert parent is self._capture
        if children:
            self._slots.add_content("", children)

    @contextmanager
    def slot(self, slot: str = "") -> Iterator[None]:
        capture = ElementNonEmpty("__capture__")
        push_element_context(capture)
        try:
            yield
        finally:
            parent, children = pop_element_context()
            assert parent is capture
            self._slots.add_content(slot, children)

    def get_nodes(self) -> Iterable[Node]:
        if self._cached_nodes is None:
            # Ensure elements created by self._callback are not registered with the currently
            # active context.
            capture = ElementNonEmpty("__capture__")
            push_element_context(capture)
            result = self._callback(self._slots)
            parent, _ = pop_element_context()
            assert parent is capture
            self._cached_nodes = list(iter_nodes([result]))
        return self._cached_nodes

    def __str__(self) -> str:
        buf = io.StringIO()
        Node.render_list(buf, self.get_nodes())
        return buf.getvalue()


class ComponentWrapper(Generic[P]):
    def __init__(
        self,
        impl: ComponentImpl[P],
        slots: Sequence[str],
        default: str | None,
        styles: Sequence[Node] | None = None,
        scripts: Sequence[Node] | None = None,
    ):
        self._impl = impl
        self._slots = slots
        self._default = default
        self._styles = styles
        self._scripts = scripts

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Component:
        callback: Callable[[Slots], Node | HasNodes] = lambda slots: self._impl(
            slots, *args, **kwargs
        )
        component = Component(callback, slots=Slots(self._slots, default=self._default))
        register_with_context(component)
        if self._styles:
            register_template_styles(self._styles)
        if self._scripts:
            register_template_scripts(self._scripts)
        return component


def component(
    slots: Sequence[str] | None = None,
    default: str | None = None,
    style: Node | Sequence[Node] | None = None,
    script: Node | Sequence[Node] | None = None,
) -> Callable[[ComponentImpl[P]], ComponentWrapper[P]]:
    slots = slots or []
    if default and not slots:
        raise ValueError(f"Can't set default without slots: {default!r}")
    elif default and default not in slots:
        raise ValueError(
            f"Invalid default: {default!r}. Available slots: {', '.join(repr(s) for s in slots)}"
        )

    styles = [style] if isinstance(style, Node) else style
    scripts = [script] if isinstance(script, Node) else script

    def decorator(fn: ComponentImpl[P]) -> ComponentWrapper[P]:
        return ComponentWrapper(
            fn, slots=slots, default=default, styles=styles, scripts=scripts
        )

    return decorator
