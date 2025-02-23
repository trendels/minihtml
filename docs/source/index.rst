.. minihtml documentation master file, created by
   sphinx-quickstart on Sun Feb 23 13:23:21 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

minihtml
========

``minihtml`` is a library to generate HTML documents from Python. It aims to
provide an API that allows you to define the structure of an HTML document in a
succinct and natural way.

By building up nested HTML elements using context managers, you can combine
HTML generation with control flow statements in a way that is easy to read and
does not obscure the structure of the resulting HTML document.

For example, this code:

.. literalinclude:: ../../examples/hello_world.py
   :language: python

produces this HTML:

.. literalinclude:: ../../examples/hello_world.html
   :language: html

The short example above already shows a few key features of the API:

- **declarative API**: Using the declarative style, you can use regular ``for``
  loops and other control flow statements to build up nested elements:

  >>> from minihtml.tags import ul, li
  >>> with ul as ingredients:
  ...     for item in ("bacon", "lettuce", "tomato"):
  ...         li(item)
  <...>
  >>> print(ingredients)
  <ul>
    <li>bacon</li>
    <li>lettuce</li>
    <li>tomato</li>
  </ul>

  You can also use a list comprehension of course, but this tends to only work
  for very simple examples. As soon as you start nesting loops or have inline
  conditionals, readability suffers.

  >>> ingredients = ul(*[li(item) for item in ("bacon", "lettuce", "tomato")])
  >>> print(ingredients)
  <ul>
    <li>bacon</li>
    <li>lettuce</li>
    <li>tomato</li>
  </ul>

  .. workaround for broken highlighting in vim*

- **fluent API**: Operations on elements can be chained to write code that is
  close to the generated HTML:

  >>> from minihtml.tags import a
  >>> link = a(href="http://example.com/")("My Website")
  >>> print(link)
  <a href="http://example.com/">My Website</a>

- **shortcuts**: There are convenient shortcuts to set the common HTML
  attributes `id` and `class`:

  >>> from minihtml.tags import div
  >>> content = div["#content text-xl font-bold"]
  >>> print(content)
  <div id="content" class="text-xl font-bold"></div>

- **pretty printing**: All HTML output is pretty-printed (indented) for easier
  debugging.

Some additional features:

- A flexible :ref:`component system <components>` with optional :ref:`tracking of JS and CSS dependencies <collecting>`.

- Helpers for :ref:`creating re-useable template with layouts <templates>` and
  :ref:`making contextual data available in templates <context>`.

- Comes with type annotations for the entire API (for use with type checkes
  such as `mypy <https://mypy-lang.org/>`_ or `pyright
  <https://microsoft.github.io/pyright>`_).

Continue reading at :ref:`basics` to learn more.

.. toctree::
   :maxdepth: 2
   :hidden:

   basics
   components
   templates
   context
   api
   tags

.. toctree::
   :hidden:
   :caption: Meta

   PyPI <https://pypi.org/project/minihtml/>
   GitHub <https://github.com/trendels/minihtml/>
   Changelog <https://github.com/trendels/minihtml/blob/main/Changelog.md>
