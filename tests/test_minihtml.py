import pytest
from minihtml import Html, tostring
from pytest import raises as assert_raises


@pytest.fixture
def h():
    return Html()


def test_tags(h: Html):
    tag = h.html(h.title("hello, world!"))
    assert str(tag) == "<html><title>hello, world!</title></html>"


def test_attributes(h: Html):
    tag_one = h.a(href="/foo")("Foo")
    tag_two = h.a("Foo", href="/foo")
    assert str(tag_one) == str(tag_two) == '<a href="/foo">Foo</a>'


def test_attributes_name_mangling(h: Html):
    assert str(h.span(class_="myclass")) == '<span class="myclass"></span>'
    assert str(h.span(data_foo="bar")) == '<span data-foo="bar"></span>'
    assert str(h.span(_="quux")) == '<span _="quux"></span>'


def test_name_only_attributes(h: Html):
    tag = h.input(disabled=True, invisibile=False)
    assert str(tag) == "<input disabled />"


def test_empty(h: Html):
    assert str(h.br) == "<br />"

    with assert_raises(TypeError):
        h.br("content")


def test_class_and_id(h: Html):
    tag = h.div["#my-id class-1 class-2"]
    assert str(tag) == '<div id="my-id" class="class-1 class-2"></div>'


def test_text_types(h: Html):
    assert str(h.span("1")) == "<span>1</span>"
    assert str(h.span(1)) == "<span>1</span>"
    assert str(h.span(1.0)) == "<span>1.0</span>"
    assert str(h.span(h.raw("raw"))) == "<span>raw</span>"


def test_escape(h: Html):
    assert str(h.span('"<>"')) == '<span>"&lt;&gt;"</span>'
    assert str(h.span(x='"<>"')) == '<span x="&quot;&lt;&gt;&quot;"></span>'
    assert str(h.span['">']) == '<span class="&quot;&gt;"></span>'
    assert str(h.span['#">']) == '<span id="&quot;&gt;"></span>'


def test_raw(h: Html):
    assert str(h.raw('<>""')) == '<>""'
    tag = h.p(h.raw("<script>alert('boo!');</script>"))
    assert str(tag) == "<p><script>alert('boo!');</script></p>"


def test_tostring(h: Html):
    tag = h.html(h.p("hello"))

    s = tostring(tag)
    assert s == "<!doctype html>\n<html><p>hello</p></html>\n"

    s = tostring(tag, doctype="<!DOCTYPE html>")
    assert s == "<!DOCTYPE html>\n<html><p>hello</p></html>\n"


def test_tag_repr(h: Html):
    assert repr(h.p("hi")) == "<MixedElement 'p'>"
