import io
import re
import sys
from collections.abc import Iterable, Iterator
from contextvars import ContextVar
from dataclasses import dataclass
from html import escape
from itertools import zip_longest
from typing import Literal, Protocol, TextIO, overload

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# We also disallow '&', '<', ';'
ATTRIBUTE_NAME_RE = re.compile(r"^[a-zA-Z0-9!#$%()*+,.:?@\[\]^_`{|}~-]+$")


class CircularReferenceError(Exception):
    """
    Raised when a circular reference between elements is detected.
    """

    pass


class Node:
    """
    Base class for text nodes and elements.
    """

    _inline: bool

    def write(self, f: TextIO, indent: int = 0) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        buffer = io.StringIO()
        self.write(buffer)
        return buffer.getvalue()

    @staticmethod
    def render_list(f: TextIO, nodes: Iterable["Node"]) -> None:
        node_list = list(nodes)
        for node, next_ in zip_longest(node_list, node_list[1:]):
            node.write(f)
            if next_ is not None:
                if node._inline != next_._inline or not (node._inline or next_._inline):
                    f.write("\n")


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
    """
    A text node.

    Use the :func:`text` and :func:`safe` functions to create text nodes.
    """

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
    """
    Create a text node.

    When called inside an element context, adds text content to the parent
    element.
    """
    node = Text(s)
    register_with_context(node)
    return node


def safe(s: str) -> Text:
    """
    Create a text node with HTML escaping disabled.

    When called inside an element context, adds text content to the parent
    element.
    """
    node = Text(s, escape=False)
    register_with_context(node)
    return node


def _format_attrs(attrs: dict[str, str]) -> str:
    return " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attrs.items())


class Element(Node):
    """
    Base class for elements.
    """

    _tag: str
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

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._tag}>"


class ElementEmpty(Element):
    """
    An empty element.
    """

    def __init__(self, tag: str, *, inline: bool = False, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag
        self._attrs: dict[str, str] = {}

    def __call__(self, **attrs: str | bool) -> Self:
        for name, value in attrs.items():
            name = name if name == "_" else name.rstrip("_").replace("_", "-")
            if not ATTRIBUTE_NAME_RE.fullmatch(name):
                raise ValueError(f"Invalid attribute name: {name!r}")
            if value is True:
                self._attrs[name] = name
            elif value is not False:
                self._attrs[name] = value

        return self

    def write(self, f: TextIO, indent: int = 0) -> None:
        attrs = f" {_format_attrs(self._attrs)}" if self._attrs else ""
        if self._omit_end_tag:
            f.write(f"<{self._tag}{attrs}>")
        else:
            f.write(f"<{self._tag}{attrs}></{self._tag}>")


class ElementNonEmpty(Element):
    """
    An element that can have content.
    """

    def __init__(self, tag: str, *, inline: bool = False):
        self._tag = tag
        self._attrs: dict[str, str] = {}
        self._children: list[Node] = []
        self._inline = inline

    def __call__(self, *content: Node | HasNodes | str, **attrs: str | bool) -> Self:
        for name, value in attrs.items():
            name = name if name == "_" else name.rstrip("_").replace("_", "-")
            if not ATTRIBUTE_NAME_RE.fullmatch(name):
                raise ValueError(f"Invalid attribute name: {name!r}")
            if value is True:
                self._attrs[name] = name
            elif value is not False:
                self._attrs[name] = value

        for obj in content:
            if not isinstance(obj, str):
                deregister_from_context(obj)
        self._children.extend(iter_nodes(content))

        return self

    def __enter__(self) -> Self:
        push_element_context(self)
        return self

    def __exit__(self, *exc_info: object) -> None:
        parent, content = pop_element_context()
        assert parent is self
        parent(*content)

    def write(self, f: TextIO, indent: int = 0) -> None:
        ids_seen = _rendering_context.get(None)
        if ids_seen is not None:
            if id(self) in ids_seen:
                raise CircularReferenceError
            ids_seen.add(id(self))
        else:
            ids_seen = {id(self)}
            _rendering_context.set(ids_seen)

        try:
            inline_mode = self._inline or all([c._inline for c in self._children])
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
        finally:
            ids_seen.remove(id(self))


@dataclass(slots=True)
class ElementContext:
    parent: ElementNonEmpty
    collected_content: list[Node | HasNodes]
    registered_content: set[Node | HasNodes]


_context_stack = ContextVar[list[ElementContext]]("context_stack")
_rendering_context = ContextVar[set[int]]("rendering_context")


def push_element_context(parent: ElementNonEmpty) -> None:
    ctx = ElementContext(parent=parent, collected_content=[], registered_content=set())
    if stack := _context_stack.get(None):
        stack.append(ctx)
    else:
        _context_stack.set([ctx])


def pop_element_context() -> tuple[ElementNonEmpty, list[Node | HasNodes]]:
    ctx = _context_stack.get().pop()
    return ctx.parent, [
        obj for obj in ctx.collected_content if obj in ctx.registered_content
    ]


def register_with_context(obj: Node | HasNodes) -> None:
    if stack := _context_stack.get(None):
        ctx = stack[-1]
        if obj not in ctx.registered_content:
            ctx.registered_content.add(obj)
            ctx.collected_content.append(obj)


def deregister_from_context(obj: Node | HasNodes) -> None:
    if stack := _context_stack.get(None):
        ctx = stack[-1]
        ctx.registered_content.discard(obj)


class Fragment:
    """
    A collection of nodes without a parent element.

    Use the :func:`fragment` function to create fragments.
    """

    def __init__(self, *content: Node | HasNodes | str):
        self._content = list(content)
        for obj in content:
            if not isinstance(obj, str):
                deregister_from_context(obj)

    def get_nodes(self) -> Iterable[Node]:
        return iter_nodes(self._content)

    def __enter__(self) -> Self:
        self._capture = ElementNonEmpty("__capture__")
        push_element_context(self._capture)
        return self

    def __exit__(self, *exc_info: object) -> None:
        parent, content = pop_element_context()
        assert parent is self._capture
        self._content.extend(content)

    def __str__(self) -> str:
        buf = io.StringIO()
        Node.render_list(buf, self.get_nodes())
        return buf.getvalue()


def fragment(*content: Node | HasNodes | str) -> Fragment:
    """
    Create a fragment.

    A fragment is a collection of nodes without a parent element.

    When called inside an element context, adds the fragment contents to the
    parent element.
    """
    f = Fragment(*content)
    register_with_context(f)
    return f


class Prototype:
    """
    Base class for element prototypes.
    """

    _tag: str

    def _get_repr(self, **flags: bool) -> str:
        flag_names = [k for k, v in flags.items() if v]
        flag_str = f" ({', '.join(flag_names)})" if flag_names else ""
        return f"<{type(self).__name__} {self._tag}{flag_str}>"


class PrototypeEmpty(Prototype):
    """
    A prototype for emtpy elements.

    Use the :func:`make_prototype` function to create new prototypes.
    """

    def __init__(self, tag: str, *, inline: bool, omit_end_tag: bool):
        self._tag = tag
        self._inline = inline
        self._omit_end_tag = omit_end_tag

    def __call__(self, **attrs: str | bool) -> ElementEmpty:
        elem = ElementEmpty(
            self._tag, inline=self._inline, omit_end_tag=self._omit_end_tag
        )(**attrs)
        register_with_context(elem)
        return elem

    def __getitem__(self, key: str) -> ElementEmpty:
        elem = ElementEmpty(
            self._tag, inline=self._inline, omit_end_tag=self._omit_end_tag
        )[key]
        register_with_context(elem)
        return elem

    def __repr__(self) -> str:
        return self._get_repr(inline=self._inline, omit_end_tag=self._omit_end_tag)


class PrototypeNonEmpty(Prototype):
    """
    A prototype for elements that can have content.

    Use the :func:`make_prototype` function to create new prototypes.
    """

    def __init__(self, tag: str, *, inline: bool):
        self._tag = tag
        self._inline = inline

    def __call__(
        self, *content: Node | HasNodes | str, **attrs: str | bool
    ) -> ElementNonEmpty:
        elem = ElementNonEmpty(self._tag, inline=self._inline)(*content, **attrs)
        register_with_context(elem)
        return elem

    def __getitem__(self, key: str) -> ElementNonEmpty:
        elem = ElementNonEmpty(self._tag, inline=self._inline)[key]
        register_with_context(elem)
        return elem

    def __enter__(self) -> ElementNonEmpty:
        elem = ElementNonEmpty(self._tag, inline=self._inline)
        register_with_context(elem)
        push_element_context(elem)
        return elem

    def __exit__(self, *exc_info: object) -> None:
        parent, content = pop_element_context()
        parent(*content)

    def __repr__(self) -> str:
        return self._get_repr(inline=self._inline)


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
    """
    Factory function to create a new element prototype.

    Args:
        tag: The tag name.
        inline: Whether or not the element is an inline (``True``) or block
          element (``False``).
        empty: Whether or not the element is allowed to have content.
        omit_end_tag: When `empty=True`, whether or not the end tag should be
          omitted when rendering.

    Returns:
        An element prototype.
    """
    if empty:
        return PrototypeEmpty(tag, inline=inline, omit_end_tag=omit_end_tag)
    return PrototypeNonEmpty(tag, inline=inline)
