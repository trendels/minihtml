from html import escape
from typing import Dict, List, Union, TypeVar

__version__ = "0.1.2"

Text = Union[str, int, float, "RawText"]
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


_T = TypeVar("_T", bound="Tag")

class Tag:
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
                str(c) if isinstance(c, Tag) else escape(str(c), quote=False)
                for c in self.children
            ]),
        )

    def __repr__(self) -> str:
        return "<{} {!r}>".format(type(self).__name__, self.name)


_MT = TypeVar("_MT", bound="MixedTag")

class MixedTag(Tag):
    """
    An HTML tag that can contain a mix of text and other elements.
    """

    def __call__(
        self: _MT,
        *children: Union["Tag", Text],
        **attributes: AttributeValue,
    ) -> _MT:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_ET = TypeVar("_ET", bound="EmptyTag")

class EmptyTag(Tag):
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

class TextOnlyTag(Tag):
    """
    An HTML tag that contains only text content.
    """
    def __call__(self: _TO, *children: Text, **attributes: AttributeValue) -> _TO:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_NT = TypeVar("_NT", bound="NoTextTag")

class NoTextTag(Tag):
    """
    An HTML tag that contains no text content.
    """
    def __call__(self: _NT, *children: Tag, **attributes: AttributeValue) -> _NT:
        self.children.extend(children)
        self._set_attributes(attributes)
        return self


_RT = TypeVar("_RT", bound="RawText")

class RawText(Tag):
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

    def _tag(self, name: str) -> MixedTag:
        return MixedTag(name)

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
    def body(self) -> MixedTag:
        return self._tag("body")

    @property
    def article(self) -> MixedTag:
        return self._tag("article")

    @property
    def section(self) -> MixedTag:
        return self._tag("section")

    @property
    def nav(self) -> MixedTag:
        return self._tag("nav")

    @property
    def aside(self) -> MixedTag:
        return self._tag("aside")

    @property
    def h1(self) -> MixedTag:
        return self._tag("h1")

    @property
    def h2(self) -> MixedTag:
        return self._tag("h2")

    @property
    def h3(self) -> MixedTag:
        return self._tag("h3")

    @property
    def h4(self) -> MixedTag:
        return self._tag("h4")

    @property
    def h5(self) -> MixedTag:
        return self._tag("h5")

    @property
    def h6(self) -> MixedTag:
        return self._tag("h6")

    @property
    def hgroup(self) -> NoTextTag:
        return self._no_text_tag("hgroup")

    @property
    def header(self) -> MixedTag:
        return self._tag("header")

    @property
    def footer(self) -> MixedTag:
        return self._tag("footer")

    @property
    def address(self) -> MixedTag:
        return self._tag("address")

    # Grouping content

    @property
    def p(self) -> MixedTag:
        return self._tag("p")

    @property
    def hr(self) -> EmptyTag:
        return self._empty_tag("hr")

    @property
    def pre(self) -> MixedTag:
        return self._tag("pre")

    @property
    def blockquote(self) -> MixedTag:
        return self._tag("blockquote")

    @property
    def ol(self) -> NoTextTag:
        return self._no_text_tag("ol")

    @property
    def ul(self) -> NoTextTag:
        return self._no_text_tag("ul")

    @property
    def li(self) -> MixedTag:
        return self._tag("li")

    @property
    def dl(self) -> NoTextTag:
        return self._no_text_tag("dl")

    @property
    def dt(self) -> MixedTag:
        return self._tag("dt")

    @property
    def dd(self) -> MixedTag:
        return self._tag("dd")

    @property
    def figure(self) -> MixedTag:
        return self._tag("figure")

    @property
    def figcaption(self) -> MixedTag:
        return self._tag("figcaption")

    @property
    def main(self) -> MixedTag:
        return self._tag("main")

    @property
    def div(self) -> MixedTag:
        return self._tag("div")

    # Text-level semantics

    @property
    def a(self) -> MixedTag:
        return self._tag("a")

    @property
    def em(self) -> MixedTag:
        return self._tag("em")

    @property
    def strong(self) -> MixedTag:
        return self._tag("strong")

    @property
    def small(self) -> MixedTag:
        return self._tag("small")

    @property
    def s(self) -> MixedTag:
        return self._tag("s")

    @property
    def cite(self) -> MixedTag:
        return self._tag("cite")

    @property
    def q(self) -> MixedTag:
        return self._tag("q")

    @property
    def dfn(self) -> MixedTag:
        return self._tag("dfn")

    @property
    def abbr(self) -> MixedTag:
        return self._tag("abbr")

    @property
    def ruby(self) -> MixedTag:
        return self._tag("ruby")

    @property
    def rt(self) -> MixedTag:
        return self._tag("rt")

    @property
    def rb(self) -> MixedTag:
        return self._tag("rb")

    @property
    def data(self) -> MixedTag:
        return self._tag("data")

    @property
    def time(self) -> MixedTag:
        return self._tag("time")

    @property
    def code(self) -> MixedTag:
        return self._tag("code")

    @property
    def var(self) -> MixedTag:
        return self._tag("var")

    @property
    def samp(self) -> MixedTag:
        return self._tag("samp")

    @property
    def kbd(self) -> MixedTag:
        return self._tag("kbd")

    @property
    def sub(self) -> MixedTag:
        return self._tag("sub")

    @property
    def sup(self) -> MixedTag:
        return self._tag("sup")

    @property
    def i(self) -> MixedTag:
        return self._tag("i")

    @property
    def b(self) -> MixedTag:
        return self._tag("b")

    @property
    def u(self) -> MixedTag:
        return self._tag("u")

    @property
    def mark(self) -> MixedTag:
        return self._tag("mark")

    @property
    def bdi(self) -> MixedTag:
        return self._tag("bdi")

    @property
    def bdo(self) -> MixedTag:
        return self._tag("bdo")

    @property
    def span(self) -> MixedTag:
        return self._tag("span")

    @property
    def br(self) -> EmptyTag:
        return self._empty_tag("br")


    @property
    def wbr(self) -> EmptyTag:
        return self._empty_tag("wbr")

    # Edits

    @property
    def ins(self) -> MixedTag:
        return self._tag("ins")

    @property
    def del_(self) -> MixedTag:
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
    def iframe(self) -> MixedTag:
        return self._tag("iframe")

    @property
    def embed(self) -> EmptyTag:
        return self._empty_tag("embed")

    @property
    def object(self) -> MixedTag:
        return self._tag("object")

    @property
    def param(self) -> EmptyTag:
        return self._empty_tag("param")

    @property
    def video(self) -> MixedTag:
        return self._tag("video")

    @property
    def audio(self) -> MixedTag:
        return self._tag("audio")

    @property
    def track(self) -> EmptyTag:
        return self._empty_tag("track")

    @property
    def map(self) -> MixedTag:
        return self._tag("map")

    @property
    def area(self) -> EmptyTag:
        return self._empty_tag("area")

    # Tabular data

    @property
    def table(self) -> NoTextTag:
        return self._no_text_tag("table")

    @property
    def caption(self) -> MixedTag:
        return self._tag("caption")

    @property
    def colgroup(self) -> NoTextTag:
        return self._no_text_tag("colgroup")

    @property
    def col(self) -> EmptyTag:
        return self._empty_tag("col")

    @property
    def tbody(self) -> NoTextTag:
        return self._no_text_tag("tbody")

    @property
    def thead(self) -> NoTextTag:
        return self._no_text_tag("thead")

    @property
    def tfoot(self) -> NoTextTag:
        return self._no_text_tag("tfoot")

    @property
    def tr(self) -> NoTextTag:
        return self._no_text_tag("tr")

    @property
    def td(self) -> MixedTag:
        return self._tag("td")

    @property
    def th(self) -> MixedTag:
        return self._tag("th")

    # Forms

    @property
    def form(self) -> MixedTag:
        return self._tag("form")

    @property
    def label(self) -> MixedTag:
        return self._tag("label")

    @property
    def input(self) -> EmptyTag:
        return self._empty_tag("input")

    @property
    def button(self) -> MixedTag:
        return self._tag("button")

    @property
    def select(self) -> NoTextTag:
        return self._no_text_tag("select")

    @property
    def datalist(self) -> MixedTag:
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
    def output(self) -> MixedTag:
        return self._tag("output")

    @property
    def progress(self) -> MixedTag:
        return self._tag("progress")

    @property
    def meter(self) -> MixedTag:
        return self._tag("meter")

    @property
    def fieldset(self) -> MixedTag:
        return self._tag("fieldset")

    @property
    def legend(self) -> MixedTag:
        return self._tag("legend")

    # Interactive elements

    @property
    def details(self) -> MixedTag:
        return self._tag("details")

    @property
    def summary(self) -> MixedTag:
        return self._tag("summary")

    @property
    def dialog(self) -> MixedTag:
        return self._tag("dialog")

    # Scripting

    @property
    def script(self) -> TextOnlyTag:
        return self._text_only_tag("script")

    @property
    def noscript(self) -> MixedTag:
        return self._tag("noscript")

    @property
    def template(self) -> MixedTag:
        return self._tag("template")

    @property
    def slot(self) -> MixedTag:
        return self._tag("slot")

    @property
    def canvas(self) -> MixedTag:
        return self._tag("canvas")


def tostring(root: Tag, doctype: str = "<!doctype html>") -> str:
    """
    Format an HTML document with docstring.
    """
    return "{}\n{}\n".format(doctype, root)
