from textwrap import dedent

from minihtml import Element
from minihtml.tags import a, body, h1, head, html, p, title


def example() -> Element:
    with html as elem:
        with head:
            title("Website Example")
        with body:
            h1("This is an example")
            p("Please visit ", a(href="https://trendels.name")("my website"), ".")

    return elem


def test_example():
    document = example()

    assert str(document) == dedent("""\
        <html>
          <head>
            <title>Website Example</title>
          </head>
          <body>
            <h1>This is an example</h1>
            <p>Please visit <a href="https://trendels.name">my website</a>.</p>
          </body>
        </html>""")
