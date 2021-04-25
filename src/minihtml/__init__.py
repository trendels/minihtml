from html import escape
from typing import Dict, List, Union, TypeVar

__version__ = "0.1"

Text = Union[str, int, float, "RawText"]
AttributeValue = Union[str, int, float, bool]


def _format_attributes(attributes: dict[str, AttributeValue]) -> str:
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


_B = TypeVar("_B", bound="Base")

class Base:
    """
    Base class for all tags.
    """
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.attributes: Dict[str, AttributeValue] = {}
        self.children: List[Union["Tag", Text]] = []

    def _set_attributes(self, attr: Dict[str, AttributeValue]) -> None:
        for name, value in attr.items():
            # TODO disallow leading '_' ?
            name = name.rstrip("_").replace("_", "-")
            self.attributes[name] = value

    def __getitem__(self: _B, name: str) -> _B:
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
                str(c) if isinstance(c, Base) else escape(str(c), quote=False)
                for c in self.children
            ]),
        )

    def __repr__(self) -> str:
        return "<Tag {!r}>".format(self.name)


_T = TypeVar("_T", bound="Tag")

class Tag(Base):
    """
    An HTML tag.
    """

    def __call__(
        self: _T,
        *children: Union["Tag", Text],
        **attributes: AttributeValue,
    ) -> _T:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_ET = TypeVar("_ET", bound="EmptyTag")

class EmptyTag(Base):
    """
    An HTML tag with no content.
    """
    def __call__(self: _ET, **attributes: AttributeValue) -> _ET:
        self._set_attributes(attributes)
        return self

    def __str__(self) -> str:
        return "<{name}{attributes} />".format(
            name=self.name,
            attributes=_format_attributes(self.attributes),
        )


_TO = TypeVar("_TO", bound="TextOnlyTag")

class TextOnlyTag(Base):
    """
    An HTML tag that contains only text content.
    """
    def __call__(self: _TO, *children: Text, **attributes: AttributeValue) -> _TO:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_NT = TypeVar("_NT", bound="NoTextTag")

class NoTextTag(Base):
    """
    An HTML tag that contains no text content.
    """
    def __call__(self: _NT, *children: Tag, **attributes: AttributeValue) -> _NT:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_RT = TypeVar("_RT", bound="RawText")

class RawText(Base):
    def __call__(self: _RT, *children: str) -> _RT:
        self.children.extend(children)
        return self

    def __str__(self) -> str:
        return "".join([c for c in self.children if isinstance(c, str)])


class Html:
    """
    HTML Tag factory.
    """
    def __init__(self) -> None:
        pass

    # Helper functions to pass on common arguments to tags (TBD).

    def _tag(self, name: str) -> Tag:
        return Tag(name)

    def _empty_tag(self, name: str) -> EmptyTag:
        return EmptyTag(name)
    
    def _text_only_tag(self, name: str) -> TextOnlyTag:
        return TextOnlyTag(name)
    
    def _no_text_tag(self, name: str) -> NoTextTag:
        return NoTextTag(name)

    @property
    def raw(self) -> RawText:
        return RawText("")

    # References:
    # https://html.spec.whatwg.org/multipage/#toc-semantics

    # The document element

    @property
    def html(self) -> NoTextTag:
        return self._no_text_tag("html")

    # Document metadata

    @property
    def head(self) -> NoTextTag:
        return self._no_text_tag("head")

    @property
    def title(self) -> TextOnlyTag:
        return self._text_only_tag("title")

    @property
    def base(self) -> EmptyTag:
        return self._empty_tag("base")

    @property
    def link(self) -> EmptyTag:
        return self._empty_tag("link")

    @property
    def meta(self) -> EmptyTag:
        return self._empty_tag("meta")

    @property
    def style(self) -> TextOnlyTag:
        return self._text_only_tag("style")

    # Sections

    @property
    def body(self) -> Tag:
        return self._tag("body")

    @property
    def article(self) -> Tag:
        return self._tag("article")

    @property
    def section(self) -> Tag:
        return self._tag("section")

    @property
    def nav(self) -> Tag:
        return self._tag("nav")

    @property
    def aside(self) -> Tag:
        return self._tag("aside")

    @property
    def h1(self) -> Tag:
        return self._tag("h1")

    @property
    def h2(self) -> Tag:
        return self._tag("h2")

    @property
    def h3(self) -> Tag:
        return self._tag("h3")

    @property
    def h4(self) -> Tag:
        return self._tag("h4")

    @property
    def h5(self) -> Tag:
        return self._tag("h5")

    @property
    def h6(self) -> Tag:
        return self._tag("h6")

    @property
    def hgroup(self) -> NoTextTag:
        return self._no_text_tag("hgroup")

    @property
    def header(self) -> Tag:
        return self._tag("header")

    @property
    def footer(self) -> Tag:
        return self._tag("footer")

    @property
    def address(self) -> Tag:
        return self._tag("address")

    # Grouping content

    @property
    def p(self) -> Tag:
        return self._tag("p")

    @property
    def hr(self) -> EmptyTag:
        return self._empty_tag("hr")

    @property
    def pre(self) -> Tag:
        return self._tag("pre")

    @property
    def blockquote(self) -> Tag:
        return self._tag("blockquote")

    @property
    def ol(self) -> NoTextTag:
        return self._no_text_tag("ol")

    @property
    def ul(self) -> NoTextTag:
        return self._no_text_tag("ul")

    @property
    def li(self) -> Tag:
        return self._tag("li")

    @property
    def dl(self) -> NoTextTag:
        return self._no_text_tag("dl")

    @property
    def dt(self) -> Tag:
        return self._tag("dt")

    @property
    def dd(self) -> Tag:
        return self._tag("dd")

    @property
    def figure(self) -> Tag:
        return self._tag("figure")

    @property
    def figcaption(self) -> Tag:
        return self._tag("figcaption")

    @property
    def main(self) -> Tag:
        return self._tag("main")

    @property
    def div(self) -> Tag:
        return self._tag("div")

    # Text-level semantics

    @property
    def a(self) -> Tag:
        return self._tag("a")

    @property
    def em(self) -> Tag:
        return self._tag("em")

    @property
    def strong(self) -> Tag:
        return self._tag("strong")

    @property
    def small(self) -> Tag:
        return self._tag("small")

    @property
    def s(self) -> Tag:
        return self._tag("s")

    @property
    def cite(self) -> Tag:
        return self._tag("cite")

    @property
    def q(self) -> Tag:
        return self._tag("q")

    @property
    def dfn(self) -> Tag:
        return self._tag("dfn")

    @property
    def abbr(self) -> Tag:
        return self._tag("abbr")

    @property
    def ruby(self) -> Tag:
        return self._tag("ruby")

    @property
    def rt(self) -> Tag:
        return self._tag("rt")

    @property
    def rb(self) -> Tag:
        return self._tag("rb")

    @property
    def data(self) -> Tag:
        return self._tag("data")

    @property
    def time(self) -> Tag:
        return self._tag("time")

    @property
    def code(self) -> Tag:
        return self._tag("code")

    @property
    def var(self) -> Tag:
        return self._tag("var")

    @property
    def samp(self) -> Tag:
        return self._tag("samp")

    @property
    def kbd(self) -> Tag:
        return self._tag("kbd")

    @property
    def sub(self) -> Tag:
        return self._tag("sub")

    @property
    def sup(self) -> Tag:
        return self._tag("sup")

    @property
    def i(self) -> Tag:
        return self._tag("i")

    @property
    def b(self) -> Tag:
        return self._tag("b")

    @property
    def u(self) -> Tag:
        return self._tag("u")

    @property
    def mark(self) -> Tag:
        return self._tag("mark")

    @property
    def bdi(self) -> Tag:
        return self._tag("bdi")

    @property
    def bdo(self) -> Tag:
        return self._tag("bdo")

    @property
    def span(self) -> Tag:
        return self._tag("span")

    @property
    def br(self) -> EmptyTag:
        return self._empty_tag("br")


    @property
    def wbr(self) -> EmptyTag:
        return self._empty_tag("wbr")

    # Edits

    @property
    def ins(self) -> Tag:
        return self._tag("ins")

    @property
    def del_(self) -> Tag:
        return self._tag("del")

    # Embedded content

    @property
    def picture(self) -> NoTextTag:
        return self._no_text_tag("picture")

    @property
    def source(self) -> EmptyTag:
        return self._empty_tag("source")

    @property
    def img(self) -> EmptyTag:
        return self._empty_tag("img")

    @property
    def iframe(self) -> Tag:
        return self._tag("iframe")

    @property
    def embed(self) -> EmptyTag:
        return self._empty_tag("embed")

    @property
    def object(self) -> Tag:
        return self._tag("object")

    @property
    def param(self) -> EmptyTag:
        return self._empty_tag("param")

    @property
    def video(self) -> Tag:
        return self._tag("video")

    @property
    def audio(self) -> Tag:
        return self._tag("audio")

    @property
    def track(self) -> EmptyTag:
        return self._empty_tag("track")

    @property
    def map(self) -> Tag:
        return self._tag("map")

    @property
    def area(self) -> EmptyTag:
        return self._empty_tag("area")

    # Tabular data

    @property
    def form(self) -> Tag:
        return self._tag("form")

    @property
    def label(self) -> Tag:
        return self._tag("label")

    @property
    def input(self) -> EmptyTag:
        return self._empty_tag("input")

    @property
    def button(self) -> Tag:
        return self._tag("button")

    @property
    def select(self) -> NoTextTag:
        return self._no_text_tag("select")

    @property
    def datalist(self) -> Tag:
        return self._tag("datalist")

    @property
    def optgroup(self) -> NoTextTag:
        return self._no_text_tag("optgroup")

    @property
    def option(self) -> TextOnlyTag:
        return self._text_only_tag("option")

    @property
    def textarea(self) -> TextOnlyTag:
        return self._text_only_tag("textarea")

    @property
    def output(self) -> Tag:
        return self._tag("output")

    @property
    def progress(self) -> Tag:
        return self._tag("progress")

    @property
    def meter(self) -> Tag:
        return self._tag("meter")

    @property
    def fieldset(self) -> Tag:
        return self._tag("fieldset")

    @property
    def legend(self) -> Tag:
        return self._tag("legend")

    # Interactive elements

    @property
    def details(self) -> Tag:
        return self._tag("details")

    @property
    def summary(self) -> Tag:
        return self._tag("summary")

    @property
    def dialog(self) -> Tag:
        return self._tag("dialog")

    # Scripting

    @property
    def script(self) -> TextOnlyTag:
        return self._text_only_tag("script")

    @property
    def noscript(self) -> Tag:
        return self._tag("noscript")

    @property
    def template(self) -> Tag:
        return self._tag("template")

    @property
    def slot(self) -> Tag:
        return self._tag("slot")

    @property
    def canvas(self) -> Tag:
        return self._tag("canvas")


def tostring(root: Tag, doctype: str = "<!doctype html>") -> str:
    """
    Format an HTML document with docstring.
    """
    return "{}\n{}\n".format(doctype, root)
