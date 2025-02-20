import io
from collections.abc import Iterable, Iterator
from contextvars import ContextVar
from dataclasses import dataclass
from html import escape
from textwrap import dedent
from typing import Literal, Protocol, Self, TextIO, overload


class Node:
    _inline: bool

    def write(self, f: TextIO, indent: int = 0) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        buffer = io.StringIO()
        self.write(buffer)
        return buffer.getvalue()


class HasNodes(Protocol):
    def get_nodes(self) -> Iterable[Node]: ...  # pragma: no cover


def iter_nodes(objects: Iterable[Node | HasNodes | str]) -> Iterator[Node]:
    for obj in objects:
        match obj:
            case str(s):
                yield Text(s)
            case Node():
                yield obj
            case _:
                for node in obj.get_nodes():
                    yield node


class Text(Node):
    def __init__(self, s: str, escape: bool = True):
        self._text = s
        self._inline = True
        self._escape = escape

    def write(self, f: TextIO, indent: int = 0) -> None:
        if self._escape:
            f.write(escape(self._text, quote=False))
        else:
            f.write(self._text)


def text(s: str) -> Text:
    node = Text(s)
    register_with_context(node)
    return node


def safe(s: str) -> Text:
    node = Text(s, escape=False)
    register_with_context(node)
    return node


def _format_attrs(attrs: dict[str, str]) -> str:
    return " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attrs.items())


class Element(Node):
    _attrs: dict[str, str]

    def __getitem__(self, key: str) -> Self:
        class_names: list[str] = []
        for name in key.split():
            if name[0] == "#":
                self._attrs["id"] = name[1:]
            else:
                class_names.append(name)
        if class_names:
            old_names = self._attrs.get("class", "").split()
            self._attrs["class"] = " ".join(old_names + class_names)
        return self


class ElementEmpty(Element):
    def __init__(self, tag: str, *, inline: bool, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag
        self._attrs: dict[str, str] = {}

    def __call__(self, **attrs: str) -> Self:
        register_with_context(self)
        self._attrs.update(attrs)
        return self

    def write(self, f: TextIO, indent: int = 0) -> None:
        attrs = f" {_format_attrs(self._attrs)}" if self._attrs else ""
        if self._omit_end_tag:
            f.write(f"<{self._tag}{attrs}>")
        else:
            f.write(f"<{self._tag}{attrs}></{self._tag}>")


class ElementNonEmpty(Element):
    def __init__(self, tag: str, *, inline: bool):
        self._tag = tag
        self._attrs: dict[str, str] = {}
        self._children: list[Node] = []
        self._inline = inline

    def __call__(self, *children: Node | HasNodes | str, **attrs: str) -> Self:
        register_with_context(self)
        self._attrs.update(attrs)
        child_nodes = list(iter_nodes(children))
        for child in child_nodes:
            deregister_from_context(child)
        self._children.extend(child_nodes)
        return self

    def __enter__(self) -> Self:
        push_element_context(self)
        return self

    def __exit__(self, *exc_info: object) -> None:
        parent, children = pop_element_context()
        assert parent is self
        parent(*children)

    def write(self, f: TextIO, indent: int = 0) -> None:
        one_inline_child = len(self._children) == 1 and self._children[0]._inline
        inline_mode = self._inline or one_inline_child
        first_child_is_block = self._children and not self._children[0]._inline
        indent_next_child = not inline_mode or first_child_is_block

        attrs = f" {_format_attrs(self._attrs)}" if self._attrs else ""
        f.write(f"<{self._tag}{attrs}>")
        for node in self._children:
            if indent_next_child or not node._inline:
                f.write(f"\n{'  ' * (indent + 1)}")
            node.write(f, indent + 1)
            indent_next_child = not node._inline

        if self._children and (indent_next_child or not inline_mode):
            f.write(f"\n{'  ' * indent}")

        f.write(f"</{self._tag}>")


@dataclass(slots=True)
class ElementContext:
    parent: ElementNonEmpty
    collected_nodes: list[Node | HasNodes]
    registered_nodes: set[Node | HasNodes]


_context_stack = ContextVar[list[ElementContext]]("context_stack")


def push_element_context(parent: ElementNonEmpty) -> None:
    ctx = ElementContext(parent=parent, collected_nodes=[], registered_nodes=set())
    if stack := _context_stack.get(None):
        stack.append(ctx)
    else:
        _context_stack.set([ctx])


def pop_element_context() -> tuple[ElementNonEmpty, list[Node | HasNodes]]:
    ctx = _context_stack.get().pop()
    return ctx.parent, [
        node for node in ctx.collected_nodes if node in ctx.registered_nodes
    ]


def register_with_context(node: Node | HasNodes) -> None:
    if stack := _context_stack.get(None):
        ctx = stack[-1]
        if node not in ctx.registered_nodes:
            ctx.registered_nodes.add(node)
            ctx.collected_nodes.append(node)


def deregister_from_context(node: Node | HasNodes) -> None:
    if stack := _context_stack.get(None):
        ctx = stack[-1]
        ctx.registered_nodes.discard(node)


class fragment:
    def __init__(self, *children: Node | HasNodes | str):
        self._nodes = list(iter_nodes(children))

    def get_nodes(self) -> Iterable[Node]:
        return self._nodes

    def __str__(self) -> str:
        container = ElementNonEmpty("__container__", inline=False)(*self._nodes)
        html = str(container)
        return dedent("\n".join(html.splitlines()[1:-1]))


class PrototypeEmpty:
    def __init__(self, tag: str, *, inline: bool, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag

    def __call__(self, **attrs: str) -> ElementEmpty:
        return ElementEmpty(
            self._tag, inline=self._inline, omit_end_tag=self._omit_end_tag
        )(**attrs)

    def __getitem__(self, key: str) -> ElementEmpty:
        return ElementEmpty(
            self._tag, inline=self._inline, omit_end_tag=self._omit_end_tag
        )[key]


class PrototypeNonEmpty:
    def __init__(self, tag: str, *, inline: bool):
        self._tag = tag
        self._inline = inline

    def __call__(
        self, *children: Node | HasNodes | str, **attrs: str
    ) -> ElementNonEmpty:
        elem = ElementNonEmpty(self._tag, inline=self._inline)(*children, **attrs)
        register_with_context(elem)
        return elem

    def __getitem__(self, key: str) -> ElementNonEmpty:
        return ElementNonEmpty(self._tag, inline=self._inline)[key]

    def __enter__(self) -> ElementNonEmpty:
        elem = ElementNonEmpty(self._tag, inline=self._inline)
        push_element_context(elem)
        return elem

    def __exit__(self, *exc_info: object) -> None:
        parent, children = pop_element_context()
        parent(*children)


@overload
def make_prototype(tag: str, *, inline: bool = ...) -> PrototypeNonEmpty: ...


@overload
def make_prototype(
    tag: str, *, inline: bool = ..., empty: Literal[False]
) -> PrototypeNonEmpty: ...


@overload
def make_prototype(
    tag: str, *, inline: bool = ..., empty: Literal[True], omit_end_tag: bool = ...
) -> PrototypeEmpty: ...


def make_prototype(
    tag: str, *, inline: bool = False, empty: bool = False, omit_end_tag: bool = False
) -> PrototypeNonEmpty | PrototypeEmpty:
    if empty:
        return PrototypeEmpty(tag, inline=inline, omit_end_tag=omit_end_tag)
    return PrototypeNonEmpty(tag, inline=inline)
