.. currentmodule:: minihtml

.. TODO The outline can be improved.

.. _basics:

Basics
======

Installation
------------

Install the `minihtml` package from PyPI:

.. code-block:: console

    $ pip install minihtml

or:

.. code-block:: console

    $ uv add minihtml

.. _prototypes:

Prototypes
----------

All minihtml HTML elements are created from a *Prototype*. A prototype is
an immutable element factory that produces :ref:`elements`.

You can import the prototypes for all HTML5 elements from :ref:`minihtml.tags <tags>`:

>>> from minihtml.tags import html, head, title
>>> html
<PrototypeNonEmpty html>

Converting an element to a string returns its HTML representation. There are
several ways to produce an element from a prototype.

Calling the prototype produces a new element:

>>> elem = html()
>>> elem
<ElementNonEmpty html>
>>> print(elem)
<html></html>

Positional arguments add content to the element. Content can be other elements
or strings:

>>> elem = html(head(title("hello, world!")))
>>> print(elem)
<html>
  <head>
    <title>hello, world!</title>
  </head>
</html>


Keyword arguments are converted to HTML :ref:`attributes <attributes>`:

>>> elem = html(lang="en")
>>> print(elem)
<html lang="en"></html>

Indexing a prototype with a string is a convenient way to set the new element's
``class`` and/or ``id`` attributes:

>>> from minihtml.tags import div
>>> elem = div["#my-id class-a class-b"]
>>> print(elem)
<div id="my-id" class="class-a class-b"></div>

Using a prototype as a context manager creates an *element context*: New
elements created within the context are added as children to the parent element
(the element returned by the context manager):

>>> with html as elem:  # creates an element context with parent element `elem` (html)
...     with head:  # creates a nested element context
...         title("hello, world!")
<...>
>>> print(elem)
<html>
  <head>
    <title>hello, world!</title>
  </head>
</html>

As you can see in the example above, it does not matter how the elements are
created, from a context manager (``with head:``) or by calling (``title()``),
they are always added to the parent element of the containing context. There is
one important exception: Elements passed as positional arguments to another
element or prototype are exempt from this, so this works as expected:

>>> from minihtml.tags import p, em
>>> with div as elem:
...     p(em("this em element is a child of p, not div"))
<...>
>>> print(elem)
<div>
  <p><em>this em element is a child of p, not div</em></p>
</div>

Finally, you can create new prototypes with the :func:`make_prototype` factory
function:

>>> from minihtml import make_prototype
>>> custom_element = make_prototype("custom-element")
>>> custom_element
<PrototypeNonEmpty custom-element>

>>> elem = custom_element()
>>> print(elem)
<custom-element></custom-element>

.. _elements:

Elements
--------

Elements provide the same APIs as :ref:`prototypes`, but they are mutable.
Calling, indexing or using an element as a context manager returns the element
itself, so all operations can be chained to modify the element further:

>>> from minihtml.tags import a
>>> elem = a["repo"](href="https://github.com/trendels/minihtml")("minihtml")
>>> print(elem)
<a class="repo" href="https://github.com/trendels/minihtml">minihtml</a>

>>> with html(lang="en") as elem:
...     with div["#main"]:
...         p("content")
<...>
>>> print(elem)
<html lang="en">
  <div id="main">
    <p>content</p>
  </div>
</html>

.. _attributes:

Attributes
----------

When setting attributes via keyword arguments, the names of keyword arguments
are modified according to these rules:

- If the name is ``_`` (a single underscore), it is not changed.
- Any trailing underscores are stripped from the name.
- Any remaining underscores are converted to hyphens (``-``).

Examples:

>>> print(div(_="something"))
<div _="something"></div>

>>> print(div(foo_bar="x"))
<div foo-bar="x"></div>

>>> from minihtml.tags import label
>>> print(label(for_="target")("Label"))
<label for="target">Label</label>

>>> print(div(__foo="bar"))
<div --foo="bar"></div>

Attribute values are quoted (HTML-escaped) automatically:

>>> print(div(attr='a value with "quotes" and a <tag>'))
<div attr="a value with &quot;quotes&quot; and a &lt;tag&gt;"></div>

.. _content:

Content
-------

We have already seen that elements and strings can be passed to elements as content.

String content is also HTML-escaped automatically. To include strings as HTML,
use the :func:`safe` helper function. Only use this if the content comes from a
trusted source, to prevent `Cross Site Scripting (XSS) vulnerabilities
<https://owasp.org/www-community/attacks/xss/>`_!

>>> print(div("content with a <tag>"))
<div>content with a &lt;tag&gt;</div>

>>> from minihtml import safe
>>> print(div(safe("<b>inline html</b>")))
<div><b>inline html</b></div>

To add text content to the parent element inside an element context, you can use the
:func:`text` helper function (:func:`safe` can be used in the same way):

>>> from minihtml import text
>>> with div as elem:
...     text("text")
...     text(" and more text")
<...>
>>> print(elem)
<div>text and more text</div>

Sometimes you might need to pass around a group of elements that do not share a
common parent element. This is called a *Fragment*. Fragments are created using
the :func:`fragment` function:

>>> from minihtml import fragment
>>> f = fragment(p("one"), p("two"), "three")
>>> print(f)
<p>one</p>
<p>two</p>
three

:func:`fragment` can also be used in an element context:

>>> with div as elem:
...     fragment(p("one"), p("two"), "three")
<...>
>>> print(elem)
<div>
  <p>one</p>
  <p>two</p>
  three
</div>
