from textwrap import dedent

from minihtml import fragment, make_prototype

div = make_prototype("div")
p = make_prototype("p")
span = make_prototype("span", inline=True)


def test_fragment_holds_a_group_of_nodes():
    f = fragment(
        p("a paragraph"),
        span("a span"),
        " and some text",
    )

    assert str(f) == dedent("""\
        <p>a paragraph</p>
        <span>a span</span> and some text""")


def test_empty_fragment_produces_no_output():
    elem = span("a", fragment(), "b")

    assert str(elem) == "<span>ab</span>"


def test_fragment_is_a_context_manager():
    with fragment() as f:
        p("hi")
        p("there")

    assert str(f) == dedent("""\
        <p>hi</p>
        <p>there</p>""")


def test_can_use_fragment_in_context_manager():
    with div as elem:
        fragment("hi there")

    assert str(elem) == "<div>hi there</div>"


def test_stringifying_fragment_has_no_side_effect():
    f = fragment()
    with f:
        p("content")

    with div as elem:
        str(f)

    assert str(elem) == "<div></div>"
