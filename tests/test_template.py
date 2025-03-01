from textwrap import dedent

from minihtml import (
    Component,
    Context,
    Element,
    Slots,
    component,
    component_scripts,
    component_styles,
    template,
    text,
)
from minihtml.tags import body, div, head, html, main, script, style, title


def test_template_renders_as_html_with_doctype_and_trailing_newline():
    @template()
    def my_template(message: str) -> Element:
        return div(message)

    assert my_template("hello").render() == dedent("""\
        <!doctype html>
        <div>hello</div>
    """)


def test_template_can_disable_doctype():
    @template()
    def my_template(message: str) -> Element:
        return div(message)

    assert my_template("hello").render(doctype=False) == "<div>hello</div>\n"


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

    @template(layout=my_layout)
    def my_template(layout: Component, message: str) -> None:
        with layout.slot("title"):
            text("my title")
        div(message)

    assert my_template("hello").render() == dedent("""\
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

    # Test that layout is not cached
    assert my_template("goodbye").render() == dedent("""\
        <!doctype html>
        <html>
          <head>
            <title>my title</title>
          </head>
          <body>
            <div id="content">
              <div>goodbye</div>
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

    @component(
        style=style("main { background: #eee }"),
        script=script("// layout script goes here"),
    )
    def my_layout(slots: Slots) -> Element:
        with html as elem:
            with head:
                component_styles()
            with body:
                with main:
                    slots.slot()
                component_scripts()

        return elem

    @template(layout=my_layout)
    def my_template(layout: Component) -> None:
        my_component()
        my_component()

    assert my_template().render() == dedent("""\
        <!doctype html>
        <html>
          <head>
            <style>main { background: #eee }</style>
            <style>.my-component { background: #ccc }</style>
          </head>
          <body>
            <main>
              <div class="my-component"></div>
              <div class="my-component"></div>
            </main>
            <script>// layout script goes here</script>
            <script>// 1st script goes here</script>
            <script>// 2nd script goes here</script>
          </body>
        </html>
    """)


def test_passing_component_styles_and_scripts_as_arguments():
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
        return html(
            head(
                component_styles(),
            ),
            body(
                my_component(),
                my_component(),
                component_scripts(),
            ),
        )

    assert my_template().render() == dedent("""\
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


def test_template_is_rendered_lazily():
    class MyContext(Context):
        def __init__(self, name: str):
            self.name = name

    @template()
    def my_template() -> Element:
        return div(MyContext.get().name)

    t = my_template()

    with MyContext(name="fred"):
        assert t.render(doctype=False) == "<div>fred</div>\n"

    with MyContext(name="barney"):
        assert t.render(doctype=False) == "<div>barney</div>\n"
