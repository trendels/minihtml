from textwrap import dedent

from minihtml import Component, Element, Slots, component, template, text
from minihtml.tags import body, div, head, html, title


def test_template_returns_html_with_doctype_and_trailing_newline():
    @template()
    def my_template(message: str) -> Element:
        return div(message)

    assert my_template("hello") == dedent("""\
        <!doctype html>
        <div>hello</div>
    """)


def test_template_can_disable_doctype():
    @template(doctype=False)
    def my_template(message: str) -> Element:
        return div(message)

    assert my_template("hello") == dedent("""\
        <div>hello</div>
    """)


def test_template_with_layout_component():
    @component(slots=["title", "content"], default="content")
    def my_layout(slots: Slots) -> Element:
        with html as elem:
            with head, title:
                slots.slot("title")
            with body:
                with div["#content"]:
                    slots.slot()

        return elem

    @template(layout=my_layout())
    def my_template(layout: Component, message: str) -> None:
        with layout.slot("title"):
            text("my title")
        div(message)

    assert my_template("hello") == dedent("""\
        <!doctype html>
        <html>
          <head>
            <title>my title</title>
          </head>
          <body>
            <div id="content">
              <div>hello</div>
            </div>
          </body>
        </html>
    """)
