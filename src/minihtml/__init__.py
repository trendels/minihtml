from html import escape
from typing import Dict, List, Union, TypeVar

__version__ = "0.1.4"

TextContent = Union[str, int, float, "RawText"]
AttributeValue = Union[str, int, float, bool]


def _format_attributes(attributes: Dict[str, AttributeValue]) -> str:
    parts: List[str] = []
    for name, value in attributes.items():
        name = escape(name, quote=True)
        if isinstance(value, bool):
            if value:
                parts.append(" {}".format(name))
        else:
            value = escape(str(value), quote=True)
            parts.append(' {}="{}"'.format(name, value))
    return "".join(parts)


class Node:
    def __init__(self) -> None:
        self.children: List[Union[Node, TextContent]] = []

    def __str__(self) -> str:
        raise NotImplementedError


_T = TypeVar("_T", bound="Element")

class Element(Node):
    """
    Base class for all elements.
    """
    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__()
        self.name = name
        self.attributes: Dict[str, AttributeValue] = {}

    def _set_attributes(self, attr: Dict[str, AttributeValue]) -> None:
        for name, value in attr.items():
            if name != "_":
                # TODO disallow leading '_' ?
                name = name.rstrip("_").replace("_", "-")
            self.attributes[name] = value

    def __getitem__(self: _T, name: str) -> _T:
        class_names: List[str] = []
        for word in name.split():
            if word[0] == "#":
                self.attributes["id"] = word[1:]
            else:
                class_names.append(word)
        if class_names:
            self.attributes["class"] = " ".join(class_names)
        return self

    def __str__(self) -> str:
        return "<{name}{attributes}>{children}</{name}>".format(
            name=self.name,
            attributes=_format_attributes(self.attributes),
            children="".join([
                str(c) if isinstance(c, Node) else escape(str(c), quote=False)
                for c in self.children
            ]),
        )

    def __repr__(self) -> str:
        return "<{} {!r}>".format(type(self).__name__, self.name)


_MT = TypeVar("_MT", bound="MixedElement")

class MixedElement(Element):
    """
    An HTML elements that can contain text or other elements.
    """

    def __call__(
        self: _MT,
        *children: Union["Element", TextContent],
        **attributes: AttributeValue,
    ) -> _MT:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_ET = TypeVar("_ET", bound="EmptyElement")

class EmptyElement(Element):
    """
    An HTML element with no content.
    """
    def __call__(self: _ET, **attributes: AttributeValue) -> _ET:
        self._set_attributes(attributes)
        return self

    def __str__(self) -> str:
        return "<{name}{attributes} />".format(
            name=self.name,
            attributes=_format_attributes(self.attributes),
        )


_TO = TypeVar("_TO", bound="TextOnlyElement")

class TextOnlyElement(Element):
    """
    An HTML element that contains only text content.
    """
    def __call__(self: _TO, *children: TextContent, **attributes: AttributeValue) -> _TO:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_NT = TypeVar("_NT", bound="NoTextElement")

class NoTextElement(Element):
    """
    An HTML element that contains no text content.
    """
    def __call__(self: _NT, *children: Element, **attributes: AttributeValue) -> _NT:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_RT = TypeVar("_RT", bound="RawText")

class RawText(Node):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self: _RT, content: str) -> _RT:
        self.children.append(content)
        return self

    def __str__(self) -> str:
        return "".join(str(c) for c in self.children)


class Html:
    """
    HTML Element factory.
    """
    def __init__(self) -> None:
        pass

    # Helper functions to pass on common arguments to tags (TBD).

    def _tag(self, name: str) -> MixedElement:
        return MixedElement(name)

    def _empty_tag(self, name: str) -> EmptyElement:
        return EmptyElement(name)

    def _text_only_tag(self, name: str) -> TextOnlyElement:
        return TextOnlyElement(name)

    def _no_text_tag(self, name: str) -> NoTextElement:
        return NoTextElement(name)

    @property
    def raw(self) -> RawText:
        return RawText()

    # References:
    # https://html.spec.whatwg.org/multipage/#toc-semantics

    # The document element

    @property
    def html(self) -> NoTextElement:
        return self._no_text_tag("html")

    # Document metadata

    @property
    def head(self) -> NoTextElement:
        return self._no_text_tag("head")

    @property
    def title(self) -> TextOnlyElement:
        return self._text_only_tag("title")

    @property
    def base(self) -> EmptyElement:
        return self._empty_tag("base")

    @property
    def link(self) -> EmptyElement:
        return self._empty_tag("link")

    @property
    def meta(self) -> EmptyElement:
        return self._empty_tag("meta")

    @property
    def style(self) -> TextOnlyElement:
        return self._text_only_tag("style")

    # Sections

    @property
    def body(self) -> MixedElement:
        return self._tag("body")

    @property
    def article(self) -> MixedElement:
        return self._tag("article")

    @property
    def section(self) -> MixedElement:
        return self._tag("section")

    @property
    def nav(self) -> MixedElement:
        return self._tag("nav")

    @property
    def aside(self) -> MixedElement:
        return self._tag("aside")

    @property
    def h1(self) -> MixedElement:
        return self._tag("h1")

    @property
    def h2(self) -> MixedElement:
        return self._tag("h2")

    @property
    def h3(self) -> MixedElement:
        return self._tag("h3")

    @property
    def h4(self) -> MixedElement:
        return self._tag("h4")

    @property
    def h5(self) -> MixedElement:
        return self._tag("h5")

    @property
    def h6(self) -> MixedElement:
        return self._tag("h6")

    @property
    def hgroup(self) -> NoTextElement:
        return self._no_text_tag("hgroup")

    @property
    def header(self) -> MixedElement:
        return self._tag("header")

    @property
    def footer(self) -> MixedElement:
        return self._tag("footer")

    @property
    def address(self) -> MixedElement:
        return self._tag("address")

    # Grouping content

    @property
    def p(self) -> MixedElement:
        return self._tag("p")

    @property
    def hr(self) -> EmptyElement:
        return self._empty_tag("hr")

    @property
    def pre(self) -> MixedElement:
        return self._tag("pre")

    @property
    def blockquote(self) -> MixedElement:
        return self._tag("blockquote")

    @property
    def ol(self) -> NoTextElement:
        return self._no_text_tag("ol")

    @property
    def ul(self) -> NoTextElement:
        return self._no_text_tag("ul")

    @property
    def li(self) -> MixedElement:
        return self._tag("li")

    @property
    def dl(self) -> NoTextElement:
        return self._no_text_tag("dl")

    @property
    def dt(self) -> MixedElement:
        return self._tag("dt")

    @property
    def dd(self) -> MixedElement:
        return self._tag("dd")

    @property
    def figure(self) -> MixedElement:
        return self._tag("figure")

    @property
    def figcaption(self) -> MixedElement:
        return self._tag("figcaption")

    @property
    def main(self) -> MixedElement:
        return self._tag("main")

    @property
    def div(self) -> MixedElement:
        return self._tag("div")

    # Text-level semantics

    @property
    def a(self) -> MixedElement:
        return self._tag("a")

    @property
    def em(self) -> MixedElement:
        return self._tag("em")

    @property
    def strong(self) -> MixedElement:
        return self._tag("strong")

    @property
    def small(self) -> MixedElement:
        return self._tag("small")

    @property
    def s(self) -> MixedElement:
        return self._tag("s")

    @property
    def cite(self) -> MixedElement:
        return self._tag("cite")

    @property
    def q(self) -> MixedElement:
        return self._tag("q")

    @property
    def dfn(self) -> MixedElement:
        return self._tag("dfn")

    @property
    def abbr(self) -> MixedElement:
        return self._tag("abbr")

    @property
    def ruby(self) -> MixedElement:
        return self._tag("ruby")

    @property
    def rt(self) -> MixedElement:
        return self._tag("rt")

    @property
    def rb(self) -> MixedElement:
        return self._tag("rb")

    @property
    def data(self) -> MixedElement:
        return self._tag("data")

    @property
    def time(self) -> MixedElement:
        return self._tag("time")

    @property
    def code(self) -> MixedElement:
        return self._tag("code")

    @property
    def var(self) -> MixedElement:
        return self._tag("var")

    @property
    def samp(self) -> MixedElement:
        return self._tag("samp")

    @property
    def kbd(self) -> MixedElement:
        return self._tag("kbd")

    @property
    def sub(self) -> MixedElement:
        return self._tag("sub")

    @property
    def sup(self) -> MixedElement:
        return self._tag("sup")

    @property
    def i(self) -> MixedElement:
        return self._tag("i")

    @property
    def b(self) -> MixedElement:
        return self._tag("b")

    @property
    def u(self) -> MixedElement:
        return self._tag("u")

    @property
    def mark(self) -> MixedElement:
        return self._tag("mark")

    @property
    def bdi(self) -> MixedElement:
        return self._tag("bdi")

    @property
    def bdo(self) -> MixedElement:
        return self._tag("bdo")

    @property
    def span(self) -> MixedElement:
        return self._tag("span")

    @property
    def br(self) -> EmptyElement:
        return self._empty_tag("br")


    @property
    def wbr(self) -> EmptyElement:
        return self._empty_tag("wbr")

    # Edits

    @property
    def ins(self) -> MixedElement:
        return self._tag("ins")

    @property
    def del_(self) -> MixedElement:
        return self._tag("del")

    # Embedded content

    @property
    def picture(self) -> NoTextElement:
        return self._no_text_tag("picture")

    @property
    def source(self) -> EmptyElement:
        return self._empty_tag("source")

    @property
    def img(self) -> EmptyElement:
        return self._empty_tag("img")

    @property
    def iframe(self) -> MixedElement:
        return self._tag("iframe")

    @property
    def embed(self) -> EmptyElement:
        return self._empty_tag("embed")

    @property
    def object(self) -> MixedElement:
        return self._tag("object")

    @property
    def param(self) -> EmptyElement:
        return self._empty_tag("param")

    @property
    def video(self) -> MixedElement:
        return self._tag("video")

    @property
    def audio(self) -> MixedElement:
        return self._tag("audio")

    @property
    def track(self) -> EmptyElement:
        return self._empty_tag("track")

    @property
    def map(self) -> MixedElement:
        return self._tag("map")

    @property
    def area(self) -> EmptyElement:
        return self._empty_tag("area")

    # Tabular data

    @property
    def table(self) -> NoTextElement:
        return self._no_text_tag("table")

    @property
    def caption(self) -> MixedElement:
        return self._tag("caption")

    @property
    def colgroup(self) -> NoTextElement:
        return self._no_text_tag("colgroup")

    @property
    def col(self) -> EmptyElement:
        return self._empty_tag("col")

    @property
    def tbody(self) -> NoTextElement:
        return self._no_text_tag("tbody")

    @property
    def thead(self) -> NoTextElement:
        return self._no_text_tag("thead")

    @property
    def tfoot(self) -> NoTextElement:
        return self._no_text_tag("tfoot")

    @property
    def tr(self) -> NoTextElement:
        return self._no_text_tag("tr")

    @property
    def td(self) -> MixedElement:
        return self._tag("td")

    @property
    def th(self) -> MixedElement:
        return self._tag("th")

    # Forms

    @property
    def form(self) -> MixedElement:
        return self._tag("form")

    @property
    def label(self) -> MixedElement:
        return self._tag("label")

    @property
    def input(self) -> EmptyElement:
        return self._empty_tag("input")

    @property
    def button(self) -> MixedElement:
        return self._tag("button")

    @property
    def select(self) -> NoTextElement:
        return self._no_text_tag("select")

    @property
    def datalist(self) -> MixedElement:
        return self._tag("datalist")

    @property
    def optgroup(self) -> NoTextElement:
        return self._no_text_tag("optgroup")

    @property
    def option(self) -> TextOnlyElement:
        return self._text_only_tag("option")

    @property
    def textarea(self) -> TextOnlyElement:
        return self._text_only_tag("textarea")

    @property
    def output(self) -> MixedElement:
        return self._tag("output")

    @property
    def progress(self) -> MixedElement:
        return self._tag("progress")

    @property
    def meter(self) -> MixedElement:
        return self._tag("meter")

    @property
    def fieldset(self) -> MixedElement:
        return self._tag("fieldset")

    @property
    def legend(self) -> MixedElement:
        return self._tag("legend")

    # Interactive elements

    @property
    def details(self) -> MixedElement:
        return self._tag("details")

    @property
    def summary(self) -> MixedElement:
        return self._tag("summary")

    @property
    def dialog(self) -> MixedElement:
        return self._tag("dialog")

    # Scripting

    @property
    def script(self) -> TextOnlyElement:
        return self._text_only_tag("script")

    @property
    def noscript(self) -> MixedElement:
        return self._tag("noscript")

    @property
    def template(self) -> MixedElement:
        return self._tag("template")

    @property
    def slot(self) -> MixedElement:
        return self._tag("slot")

    @property
    def canvas(self) -> MixedElement:
        return self._tag("canvas")


def tostring(root: Element, doctype: str = "<!doctype html>") -> str:
    """
    Format an HTML document with docstring.
    """
    return "{}\n{}\n".format(doctype, root)
