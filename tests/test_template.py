from textwrap import dedent

from minihtml import (
    Component,
    Element,
    Slots,
    component,
    component_scripts,
    component_styles,
    template,
    text,
)
from minihtml.tags import body, div, head, html, script, style, title


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


def test_template_collects_and_deduplicates_component_styles_and_scripts():
    @component(
        style=style(".my-component { background: #ccc }"),
        script=[
            script("// 1st script goes here"),
            script("// 2nd script goes here"),
        ],
    )
    def my_component(slots: Slots) -> Element:
        return div["my-component"]

    @template()
    def my_template() -> Element:
        with html as elem:
            with head:
                component_styles()
            with body:
                my_component()
                my_component()
                component_scripts()

        return elem

    assert my_template() == dedent("""\
        <!doctype html>
        <html>
          <head>
            <style>.my-component { background: #ccc }</style>
          </head>
          <body>
            <div class="my-component"></div>
            <div class="my-component"></div>
            <script>// 1st script goes here</script>
            <script>// 2nd script goes here</script>
          </body>
        </html>
    """)
