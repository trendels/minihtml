import io
from collections.abc import Iterable, Iterator
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
    def __init__(self, text: str):
        self._text = text
        self._inline = True

    def write(self, f: TextIO, indent: int = 0) -> None:
        f.write(self._text)


class Element(Node):
    def __init__(self, tag: str, *, inline: bool):
        self._tag = tag
        self._children: list[Node] = []
        self._inline = inline

    def __call__(self, *children: Node | HasNodes | str) -> Self:
        self._children.extend(iter_nodes(children))
        return self

    def write(self, f: TextIO, indent: int = 0) -> None:
        one_inline_child = len(self._children) == 1 and self._children[0]._inline
        inline_mode = self._inline or one_inline_child
        first_child_is_block = self._children and not self._children[0]._inline
        indent_next_child = not inline_mode or first_child_is_block

        f.write(f"<{self._tag}>")
        for node in self._children:
            if indent_next_child or not node._inline:
                f.write(f"\n{'  ' * (indent + 1)}")
            node.write(f, indent + 1)
            indent_next_child = not node._inline

        if self._children and (indent_next_child or not inline_mode):
            f.write(f"\n{'  ' * indent}")

        f.write(f"</{self._tag}>")


class EmptyElement(Node):
    def __init__(self, tag: str, *, inline: bool, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag

    def write(self, f: TextIO, indent: int = 0) -> None:
        if self._omit_end_tag:
            f.write(f"<{self._tag}>")
        else:
            f.write(f"<{self._tag}></{self._tag}>")


class fragment:
    def __init__(self, *children: Node | HasNodes | str):
        self._nodes = list(iter_nodes(children))

    def get_nodes(self) -> Iterable[Node]:
        return self._nodes

    def __str__(self) -> str:
        container = Element("__container__", inline=False)(*self._nodes)
        html = str(container)
        return dedent("\n".join(html.splitlines()[1:-1]))


class Prototype:
    def __init__(self, tag: str, *, inline: bool):
        self._tag = tag
        self._inline = inline

    def __call__(self, *children: Node | HasNodes | str) -> Element:
        return Element(self._tag, inline=self._inline)(*children)


class EmptyPrototype:
    def __init__(self, tag: str, *, inline: bool, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag

    def __call__(self) -> EmptyElement:
        return EmptyElement(
            self._tag, inline=self._inline, omit_end_tag=self._omit_end_tag
        )


@overload
def make_prototype(tag: str, *, inline: bool = ...) -> Prototype: ...


@overload
def make_prototype(
    tag: str, *, inline: bool = ..., empty: Literal[False]
) -> Prototype: ...


@overload
def make_prototype(
    tag: str, *, inline: bool = ..., empty: Literal[True], omit_end_tag: bool = ...
) -> EmptyPrototype: ...


def make_prototype(
    tag: str, *, inline: bool = False, empty: bool = False, omit_end_tag: bool = False
) -> Prototype | EmptyPrototype:
    if empty:
        return EmptyPrototype(tag, inline=inline, omit_end_tag=omit_end_tag)
    return Prototype(tag, inline=inline)
