from textwrap import dedent

import pytest
from pytest import raises as assert_raises

from minihtml import CircularReferenceError, make_prototype, safe, text

div = make_prototype("div")
span = make_prototype("span", inline=True)
img = make_prototype("img", inline=True, empty=True, omit_end_tag=True)
iframe = make_prototype("iframe", empty=True, omit_end_tag=False)


def test_prototype_repr():
    assert repr(div) == "<PrototypeNonEmpty div>"
    assert repr(img) == "<PrototypeEmpty img>"


def test_element_repr():
    assert repr(div()) == "<ElementNonEmpty div>"
    assert repr(img()) == "<ElementEmpty img>"


def test_render_bare_elements():
    assert str(div()) == "<div></div>"
    assert str(img()) == "<img>"
    assert str(iframe()) == "<iframe></iframe>"


def test_positional_args_are_children():
    assert str(span(img())) == "<span><img></span>"
    assert str(span("hello")) == "<span>hello</span>"


def test_keyword_args_are_attributes():
    assert str(div(title="hello")) == '<div title="hello"></div>'
    assert str(img(src="hello.png")) == '<img src="hello.png">'


@pytest.mark.parametrize(
    ("kwarg", "attribute"),
    [
        ("foo", "foo"),
        ("foo_bar", "foo-bar"),
        ("foo__bar", "foo--bar"),
        ("_foo", "-foo"),
        ("__foo", "--foo"),
        ("foo_", "foo"),
        ("foo__", "foo"),
        ("_", "_"),
    ],
)
def test_attribute_name_mangling(kwarg: str, attribute: str):
    assert str(div(**{kwarg: "test"})) == f'<div {attribute}="test"></div>'
    assert str(img(**{kwarg: "test"})) == f'<img {attribute}="test">'


def test_boolean_attributes():
    assert str(div(enabled=True)) == '<div enabled="enabled"></div>'
    assert str(div(enabled=False)) == "<div></div>"
    assert str(div(_=True)) == '<div _="_"></div>'
    assert str(div(_=False)) == "<div></div>"

    assert str(img(enabled=True)) == '<img enabled="enabled">'
    assert str(img(enabled=False)) == "<img>"
    assert str(img(_=True)) == '<img _="_">'
    assert str(img(_=False)) == "<img>"


def test_attribute_values_are_escaped():
    assert (
        str(div(title='hello"<world>&'))
        == '<div title="hello&quot;&lt;world&gt;&amp;"></div>'
    )


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        '"',
        "'",
        "/",
        "=",
        ">",
        "a a",
        'a"a',
        "a'a",
        "a/a",
        "a>a",
    ],
)
def test_attribute_names_are_validated(name: str):
    with assert_raises(ValueError, match=f"Invalid attribute name: {name!r}"):
        div(**{name: "test"})

    with assert_raises(ValueError, match=f"Invalid attribute name: {name!r}"):
        img(**{name: "test"})


def test_text_contend_is_escaped():
    assert str(div('hello"<world>&')) == '<div>hello"&lt;world&gt;&amp;</div>'


def test_indexing_adds_class_names():
    assert str(div["green"]) == '<div class="green"></div>'
    assert str(div["green supergreen"]) == '<div class="green supergreen"></div>'
    assert str(div["green"]["supergreen"]) == '<div class="green supergreen"></div>'
    assert str(img["myclass"]) == '<img class="myclass">'
    assert str(img["myclass"]["otherclass"]) == '<img class="myclass otherclass">'


def test_indexing_sets_hashtag_id():
    assert str(div["#blue"]) == '<div id="blue"></div>'
    assert str(div["green #blue"]) == '<div id="blue" class="green"></div>'
    assert str(div["green #blue #red"]) == '<div id="red" class="green"></div>'
    assert str(img["#my-id"]) == '<img id="my-id">'


def test_calling_prototype_in_element_context_adds_child_element():
    with div as elem:
        span("hello")

    assert str(elem) == "<div><span>hello</span></div>"

    with div["myclass"] as elem:
        span("hello")(" again")

    assert str(elem) == '<div class="myclass"><span>hello again</span></div>'

    with div["myclass"] as elem:
        img(src="hello.png")

    assert str(elem) == '<div class="myclass"><img src="hello.png"></div>'


def test_calling_element_in_element_context_adds_child_element():
    with div as elem:
        span["test"]("hello")

    assert str(elem) == '<div><span class="test">hello</span></div>'

    with div["myclass"] as elem:
        span["test"]("hello again")

    assert (
        str(elem) == '<div class="myclass"><span class="test">hello again</span></div>'
    )

    with div["myclass"] as elem:
        img["test"](src="hello.png")

    assert str(elem) == '<div class="myclass"><img class="test" src="hello.png"></div>'


def test_elements_used_as_positional_args_are_not_added_twice():
    with div as elem:
        div["nested"](span("hello"))

    assert str(elem) == dedent("""\
        <div>
          <div class="nested"><span>hello</span></div>
        </div>""")

    with div["myclass"] as elem:
        div["nested"](span("hello")(" again"))

    assert str(elem) == dedent("""\
        <div class="myclass">
          <div class="nested"><span>hello again</span></div>
        </div>""")


def test_context_managers_can_be_nested():
    with div["outer"] as elem:
        with div, div["inner"]:
            span("hello")

    assert str(elem) == dedent("""\
        <div class="outer">
          <div>
            <div class="inner"><span>hello</span></div>
          </div>
        </div>""")


def test_context_manager_with_text_content():
    with div as elem:
        text("hello")
        safe("<!-- this is a comment -->")

    assert str(elem) == "<div>hello<!-- this is a comment --></div>"


def test_circular_reference_raises_error_when_rendering():
    elem = div()
    elem(elem)

    with assert_raises(CircularReferenceError):
        str(elem)

    with div() as elem2:
        elem2()

    with assert_raises(CircularReferenceError):
        str(elem2)
