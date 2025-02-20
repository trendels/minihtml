from textwrap import dedent

from minihtml import fragment, make_prototype


def test_nested_block_elements_are_rendered_with_indentation():
    div = make_prototype("div")

    assert str(div(div())) == dedent(
        """\
        <div>
          <div></div>
        </div>"""
    )
    assert str(div(div(), div())) == dedent(
        """\
        <div>
          <div></div>
          <div></div>
        </div>"""
    )


def test_nested_inline_elements_are_rendered_without_indentation():
    span = make_prototype("span", inline=True)
    em = make_prototype("em", inline=True)

    assert str(span(em())) == "<span><em></em></span>"
    assert str(span(em(), em())) == "<span><em></em><em></em></span>"


def test_consecutive_inline_children_of_block_elements_are_rendered_without_indentation():
    div = make_prototype("div")
    span = make_prototype("span", inline=True)

    assert str(div(span(), span())) == dedent("<div><span></span><span></span></div>")


def test_a_single_inline_child_of_a_block_element_is_rendered_without_indentation():
    div = make_prototype("div")
    span = make_prototype("span", inline=True)

    assert str(div(span())) == "<div><span></span></div>"


def test_nested_block_elements_are_always_rendered_with_indentation():
    div = make_prototype("div")
    p = make_prototype("p")
    span = make_prototype("span", inline=True)

    assert str(div(span(), p())) == dedent(
        """\
        <div>
          <span></span>
          <p></p>
        </div>"""
    )
    assert str(div(span(), span(), p())) == dedent(
        """\
        <div>
          <span></span><span></span>
          <p></p>
        </div>"""
    )
    assert str(span(span(), p())) == dedent(
        """\
        <span><span></span>
          <p></p>
        </span>"""
    )
    assert str(span(p(), span())) == dedent(
        """\
        <span>
          <p></p>
          <span></span></span>"""
    )


def test_empty_elements_with_and_without_end_tag():
    div = make_prototype("div")
    img = make_prototype("img", inline=True, empty=True, omit_end_tag=True)
    iframe = make_prototype("iframe", empty=True, omit_end_tag=False)

    assert str(img()) == "<img>"
    assert str(iframe()) == "<iframe></iframe>"
    assert str(div(img(), img())) == "<div><img><img></div>"
    assert str(div(iframe(), iframe())) == dedent(
        """\
        <div>
          <iframe></iframe>
          <iframe></iframe>
        </div>"""
    )


def test_text_content_is_rendered_inline():
    div = make_prototype("div")
    span = make_prototype("span", inline=True)

    assert str(div("hello")) == "<div>hello</div>"
    assert str(span("hello")) == "<span>hello</span>"
    assert str(div(span(), "hello")) == "<div><span></span>hello</div>"


def test_rendering_fragments():
    div = make_prototype("div")
    span = make_prototype("span", inline=True)

    frag1 = fragment(div(), span(), "test", div())

    assert str(div(frag1)) == dedent(
        """\
        <div>
          <div></div>
          <span></span>test
          <div></div>
        </div>"""
    )

    assert str(frag1) == dedent(
        """\
        <div></div>
        <span></span>test
        <div></div>"""
    )
