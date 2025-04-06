# minihtml - Simple HTML Generation

[![PyPI - Version](https://img.shields.io/pypi/v/minihtml)](https://pypi.org/project/minihtml/)

minihtml is a library to generate HTML documents from Python. It aims to
provide an API that allows you to define the structure of an HTML document in a
succinct and natural way.

By building up nested HTML elements using context managers, you can combine
HTML generation with control flow statements in a way that is easy to read and
does not obscure the structure of the resulting HTML document.

## Installation

Install the `minihtml` package from PyPI:

    pip install minihtml

or

    uv add minihtml

## Example

A basic "hello, world" example:

~~~python
>>> from minihtml.tags import html, head, title, body, div, p, a, img
>>> with html(lang="en") as elem:
...     with head:
...         title("hello, world!")
...     with body, div["#content main"]:
...         p("Welcome to ", a(href="https://example.com/")("my website"))
...         img(src="hello.png", alt="hello")
...
<...>

>>> print(elem)
<html lang="en">
  <head>
    <title>hello, world!</title>
  </head>
  <body>
    <div id="content" class="main">
      <p>Welcome to <a href="https://example.com/">my website</a></p>
      <img src="hello.png" alt="hello">
    </div>
  </body>
</html>

~~~

## Links

- [Documentation](https://minihtml.trendels.name/)
- [Changelog](https://github.com/trendels/minihtml/blob/main/Changelog.md)
- [PyPI project page](https://pypi.org/project/minihtml/)

## License

Minihtml is released under the MIT license. See [LICENSE](LICENSE) for more information.

