.. currentmodule:: minihtml

.. _templates:

Templates
=========

A template is a helper for producing a complete HTML page.

Using templates
---------------

Create a template by using the :deco:`template` decorator on a function that
returns HTML content:

>>> from minihtml import template
>>> from minihtml.tags import html, body
>>>
>>> @template()
... def my_page():
...     return html(body("hello, world!"))
...
>>> p = my_page()
>>> p.render()
'<!doctype html>\n<html>\n  <body>hello, world!</body>\n</html>\n'

A template function returns a :class:`Template` object, which wraps the
original function. Calling the object's :meth:`Template.render` method calls
the function and returns the template rendered as a string with a ``doctype``
declaration.

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> print(p.render())
   <!doctype html>
   <html>
     <body>hello, world!</body>
   </html>

The doctype can also be disabled:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> print(p.render(doctype=False))
   <html>
     <body>hello, world!</body>
   </html>

Layout components
-----------------

Often, you will want to use a "base" template that defines a common page
structure for your project. This can be accomplished with a layout component.
Let's start with a regular component that defines an HTML page, with slots to
set the title and the page content:

>>> from minihtml import text, component
>>> from minihtml.tags import head, title, h1, p
>>>
>>> @component(slots=("title", "content"), default="content")
... def base_layout(slots):
...     with html as elem:
...         with head, title:
...             slots.slot("title")
...         with body:
...             with h1:
...                 slots.slot("title")
...             slots.slot("content")
...     return elem

We could use this component inside our template like this:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> @template()
   ... def hello():
   ...     with base_layout() as comp:
   ...         with comp.slot("title"):
   ...             text("hello, world!")
   ...         p("Welcome to my website")
   ...     return comp
   >>>
   >>> print(hello().render())
   <!doctype html>
   <html>
     <head>
       <title>hello, world!</title>
     </head>
     <body>
       <h1>hello, world!</h1>
       <p>Welcome to my website</p>
     </body>
   </html>

We can make our lives a little bit easier by assigning the ``base_layout``
component as the template's *layout component* using the ``layout`` parameter:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> @template(layout=base_layout)
   ... def hello(layout):
   ...     with layout.slot("title"):
   ...         text("hello, world!")
   ...     p("Welcome to my website")
   >>>
   >>> print(hello().render())
   <!doctype html>
   <html>
     <head>
       <title>hello, world!</title>
     </head>
     <body>
       <h1>hello, world!</h1>
       <p>Welcome to my website</p>
     </body>
   </html>

The result is the same, but the body of our template function is now shorter
and we saved a level of indentation.

Note that when using a layout component, the template will receive an instance
of the component as it's first positional argument (we called it ``layout``
above), and does not need to return anything. Instead, the template function is
executed in a ``with base_layout()`` block and all elements it creates will be
added to the layout component's default slot. For this reason, a layout
component must have a default slot and should not expect any additional
arguments.

.. _collecting:

Collecting component styles and scripts
---------------------------------------

Behind the scenes, a template will collect and deduplicate all
:ref:`component_resources` that have been associated with the components used
in the template, including the layout component.

In order to inject the collected script and style nodes into the document, you
use the :func:`component_scripts` and :func:`component_styles` placeholders. They
can appear anywhere in the template, but typically you will put
:func:`component_styles` into the ``<head>`` section of the document, and
:func:`component_scripts` either also inside ``<head>`` or at the very end of
the ``<body>`` section:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> from minihtml import component_scripts, component_styles
   >>> from minihtml.tags import style, script, div, html, head, title, body, p
   >>>
   >>> @component(
   ...     style=style(".my-card { border: 1px solid blue; }"),
   ...     script=script("console.log('welcome!');"),
   ... )
   ... def my_card(slots):
   ...     """A component with attached style and script."""
   ...     with div["my-card"] as elem:
   ...         slots.slot()
   ...     return elem
   ...
   >>> @component(style=style("body { background: #eee; }"))
   ... def my_layout(slots):
   ...     """A layout component with attached style."""
   ...     with html as elem:
   ...         with head:
   ...             title("Welcome to my website")
   ...             component_styles()  # collected styles will be inserted here
   ...         with body:
   ...             slots.slot()
   ...             component_scripts()  # collected scripts will be inserted here
   ...     return elem
   ...
   >>> @template(layout=my_layout)
   ... def my_template(layout):
   ...     with my_card():
   ...         p("First card")
   ...     with my_card():
   ...         p("Second card")
   ...
   >>> t = my_template()
   >>> print(t.render())
   <!doctype html>
   <html>
     <head>
       <title>Welcome to my website</title>
       <style>body { background: #eee; }</style>
       <style>.my-card { border: 1px solid blue; }</style>
     </head>
     <body>
       <div class="my-card">
         <p>First card</p>
       </div>
       <div class="my-card">
         <p>Second card</p>
       </div>
       <script>console.log('welcome!');</script>
     </body>
   </html>

As you can see, the script and style resources of the layout component and the
two card components have been collected, deduplicated and inserted into the
correct places.
