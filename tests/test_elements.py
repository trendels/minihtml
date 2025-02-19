from textwrap import dedent

from minihtml import make_prototype, safe, text

div = make_prototype("div")
span = make_prototype("span", inline=True)
img = make_prototype("img", inline=True, empty=True, omit_end_tag=True)
iframe = make_prototype("iframe", empty=True, omit_end_tag=False)


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


def test_attribute_values_are_escaped():
    assert (
        str(div(title='hello"<world>&'))
        == '<div title="hello&quot;&lt;world&gt;&amp;"></div>'
    )


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

    assert str(elem) == dedent("""\
        <div>
          hello<!-- this is a comment -->
        </div>""")
