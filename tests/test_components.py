from textwrap import dedent

from pytest import raises as assert_raises

from minihtml import Element, Fragment, Slots, component, fragment
from minihtml.tags import (
    body,
    div,
    h2,
    head,
    html,
    img,
    main,
    p,
    script,
    style,
    title,
)


def test_basic_component():
    @component()
    def my_component(slots: Slots, name: str) -> Element:
        with div(name=name) as elem:
            slots.slot()
        return elem

    with div["container"] as elem:
        with my_component(name="component-name"):
            p("slot content")

    assert str(elem) == dedent("""\
        <div class="container">
          <div name="component-name">
            <p>slot content</p>
          </div>
        </div>""")


def test_named_slots():
    @component(slots=("head", "main"))
    def my_component(slots: Slots) -> Element:
        with html as elem:
            with head:
                slots.slot("head")
            with body:
                with main:
                    slots.slot("main")
        return elem

    with my_component() as comp:
        with comp.slot("head"):
            title("My website")
        with comp.slot("main"):
            p("My article")

    assert str(comp) == dedent("""\
        <html>
          <head>
            <title>My website</title>
          </head>
          <body>
            <main>
              <p>My article</p>
            </main>
          </body>
        </html>""")


def test_named_slots_with_default():
    @component(slots=("head", "main"), default="main")
    def my_component(slots: Slots) -> Element:
        with html as elem:
            with head:
                slots.slot("head")
            with body:
                with main:
                    slots.slot()
        return elem

    with my_component() as comp1:
        with comp1.slot("head"):
            title("My website")
        p("My article")

    assert str(comp1) == dedent("""\
        <html>
          <head>
            <title>My website</title>
          </head>
          <body>
            <main>
              <p>My article</p>
            </main>
          </body>
        </html>""")

    with my_component() as comp2:
        with comp2.slot("head"):
            title("My website")
        with comp2.slot("main"):
            p("My article")

    assert str(comp1) == str(comp2)


def test_slot_is_filled():
    @component(slots=("icon", "main"), default="main")
    def my_component(slots: Slots) -> Element:
        with div["my-component"] as elem:
            if slots.is_filled("icon"):
                with div["icon"]:
                    slots.slot("icon")
            if slots.is_filled():
                with div["main"]:
                    slots.slot()
        return elem

    with my_component() as comp1:
        p("My article")

    assert str(comp1) == dedent("""\
        <div class="my-component">
          <div class="main">
            <p>My article</p>
          </div>
        </div>""")

    with my_component() as comp2:
        with comp2.slot("icon"):
            img(src="icon.png")

    assert str(comp2) == dedent("""\
        <div class="my-component">
          <div class="icon"><img src="icon.png"></div>
        </div>""")


def test_slots_with_default_content():
    @component(slots=("title", "content"), default="content")
    def my_component(slots: Slots) -> Fragment:
        with fragment() as f:
            with slots.slot("title"):
                h2("Default title")
            with slots.slot():
                p("Default content")
        return f

    comp1 = my_component()

    with my_component() as comp2:
        with comp2.slot("title"):
            h2("My title")
        p("My content")

    assert str(comp1) == dedent("""\
        <h2>Default title</h2>
        <p>Default content</p>""")

    assert str(comp2) == dedent("""\
        <h2>My title</h2>
        <p>My content</p>""")


def test_default_slot_must_be_a_valid_slot_name():
    with assert_raises(ValueError, match="Can't set default without slots: 'x'"):
        component(default="x")

    with assert_raises(
        ValueError, match="Invalid default: 'x'. Available slots: 'a', 'b'"
    ):
        component(slots=("a", "b"), default="x")


def test_stringifying_component_has_no_side_effect():
    @component()
    def my_component(slots: Slots) -> Element:
        with div["my-component"] as elem:
            slots.slot()
        return elem

    c1 = my_component()

    with div as elem:
        str(c1)

    assert str(elem) == "<div></div>"


def test_nested_components():
    @component()
    def inner(slots: Slots) -> Element:
        with div["inner"] as elem:
            slots.slot()
        return elem

    @component()
    def outer(slots: Slots) -> Element:
        with div["outer"] as elem:
            with inner():
                slots.slot()
        return elem

    with div["container"] as elem:
        with outer():
            p("content")

    assert str(elem) == dedent("""\
        <div class="container">
          <div class="outer">
            <div class="inner">
              <p>content</p>
            </div>
          </div>
        </div>""")


def test_component_style_and_script_has_no_effect_outside_of_template_context():
    @component(
        style=style(".my-component { background: #ccc }"),
        script=script("// script goes here"),
    )
    def my_component(slots: Slots) -> Element:
        return div["my-component"]

    assert str(my_component()) == '<div class="my-component"></div>'
