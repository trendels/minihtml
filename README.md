# minihtml - Simple HTML Generation

![PyPI - Version](https://img.shields.io/pypi/v/minihtml)

The minihtml library provides tools to generate HTML from Python. The goal of
minihtml is to enable you to write HTML mixed with presentation logic without
obscuring the structure of the resulting HTML document, not unlike the
experience with a text-based templating system such as [Jinja][jinja].

[jinja]: https://jinja.palletsprojects.com/

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
...     with body:
...         with div["#content main"]:
...             p("Welcome to ", a(href="https://example.com/")("my website"))
...             img(src="hello.png", alt="hello")
...
<ElementNonEmpty title>
<ElementNonEmpty p>
<ElementEmpty img>

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

## Prototypes and Elements

The objects you import from `minihtml.tags` are called *prototypes*. You can
think of them as HTML element factories. Prototypes are immutable. There are
several ways you can interact with a prototype to produce an actual *element*:

Calling the prototype produces an element:

~~~python
>>> print(div)
<PrototypeNonEmpty div>
>>> elem = div()
>>> repr(elem)
'<ElementNonEmpty div>'
>>> print(elem)
<div></div>

~~~

Positional arguments get converted to children of the new element, and keyword
arguments to attributes:

~~~python
>>> print(div("text"))
<div>text</div>
>>> print(div(style="background: green"))
<div style="background: green"></div>

~~~

## Element Content and Attributes

Content can be text, other elements or a mix of the two:

~~~python
>>> from minihtml.tags import em
>>> elem = div("this is ", em("emphasized text"), ".")
>>> print(elem)
<div>this is <em>emphasized text</em>.</div>

~~~

You can chain calls and all other operations on the element to modify it
further. Each operation modifies the element in-place (elements are mutable).

~~~python
>>> elem = a(href="https://github.com")("github")
>>> print(elem)
<a href="https://github.com">github</a>

~~~

Indexing is a shortcut to set the `class` and `id` attributes:

~~~python
>>> print(div["hello"])
<div class="hello"></div>
>>> print(div["#main"])
<div id="main"></div>
>>> print(div["#main foo bar"])
<div id="main" class="foo bar"></div>
>>> print(div["foo"]["bar"])
<div class="foo bar"></div>

~~~

Finally, you can build up a document declaratively by using elements or
prototypes as context managers. New elements created within the context will be
added as children to the parent element:

~~~python
>>> from minihtml.tags import ul, li
>>> with div["main"] as elem:
...     with ul:
...         for color in ("red", "green", "blue"):
...             li(color)
...
<ElementNonEmpty li>
<ElementNonEmpty li>
<ElementNonEmpty li>

>>> print(elem)
<div class="main">
  <ul>
    <li>red</li>
    <li>green</li>
    <li>blue</li>
  </ul>
</div>

~~~

Elements that are passed to another element as a positional argument are exempt
from this, so you can mix the two styles:

~~~python
>>> with div as elem:
...     p(em("this is emphasized"))
...
<ElementNonEmpty p>

# The `em` element does *not* also end up as a child of `div`.
>>> print(elem)
<div>
  <p><em>this is emphasized</em></p>
</div>

~~~

<!-- TODO document attribute name mangling -->
<!-- TODO document components -->
<!-- TODO document @template -->
