.. currentmodule:: minihtml

.. _components:

Components
==========

A component is a re-usable snippet of HTML.

Defining components
-------------------

You create components with the :deco:`component` decorator on a function.

The function always receives a :class:`Slots` objects as its first positional
argument, but can have other arguments as well.

Here is a simple component that returns a div with a configurable "name" attribute:

>>> from minihtml import component
>>> from minihtml.tags import div
>>>
>>> @component()
... def my_component(slots, name):
...     return div["my-component"](name=name)

You create an instance of the component by calling it. Like elements, a
component called inside an element context will add content to the parent
element:

>>> comp = my_component("my-name")
>>> print(comp)
<div class="my-component" name="my-name"></div>

>>> with div["container"] as elem:
...     my_component("my-name")
<...>
>>> print(elem)
<div class="container">
  <div class="my-component" name="my-name"></div>
</div>

Component slots
---------------

In addition to arguments, components can have *slots* that can be filled by the
caller with arbitrary content. So, instead of passing elements as arguments to
a component, you would use a slot. If you do not configure slots explicitly,
your component has a *default slot*.

To refer to the contents of the slot within the component definition, use the
:meth:`Slots.slot` method inside an element context. Here is a component that
wraps it's content in a ``div`` with ``class="greeting"``:

>>> @component()
... def my_greeting(slots):
...     with div["greeting"] as elem:
...         slots.slot()
...     return elem

To fill the slot of a component, use it as a context manager. Elements created
within the context are added to the default slot.

>>> from minihtml.tags import p
>>> with my_greeting() as comp:
...     p("Hello, world!")
...     p("More content.")
<...>
>>> print(comp)
<div class="greeting">
  <p>Hello, world!</p>
  <p>More content.</p>
</div>

Named slots
-----------

A component can also be declared with one or more *named slots*:

>>> @component(slots=("header", "footer"))
... def two_slots(slots):
...     with div["two-slots"] as elem:
...         with div["header"]:
...             slots.slot("header")
...         with div["footer"]:
...             slots.slot("footer")
...     return elem

To interact with a named slot, pass the slot name to :meth:`Slots.slot`, as
shown above. To fill a slot by name, use the :meth:`Component.slot`
method of the component returned by the context manager:

>>> with two_slots() as comp:
...     with comp.slot("header"):
...         p("header content")
...     with comp.slot("footer"):
...         p("footer content")
<...>
>>> print(comp)
<div class="two-slots">
  <div class="header">
    <p>header content</p>
  </div>
  <div class="footer">
    <p>footer content</p>
  </div>
</div>

Specifying a default slot
-------------------------

If your component has multiple slots, it's a good idea to define one to be the
*default slot*:

>>> from minihtml.tags import h4
>>>
>>> @component(slots=("title", "content"), default="content")
... def my_card(slots):
...     with div["my-card"] as elem:
...         with h4:
...             slots.slot("title")
...         with div["content"]:
...             slots.slot("content")
...     return elem

The default slot can always be referred to (both inside and outside of the
component definition) via it's name (as shown above), or as the unnamed default
slot:

>>> from minihtml import text
>>> with my_card() as comp:
...     with comp.slot("title"):
...         text("card title")
...     p("card content")  # this goes into the default slot ("content")
<...>
>>> print(comp)
<div class="my-card">
  <h4>card title</h4>
  <div class="content">
    <p>card content</p>
  </div>
</div>

Checking if a slot is filled
----------------------------

Inside a component, you can find out whether or not a slot has been filled
using :meth:`Slots.is_filled`:

>>> from minihtml.tags import span, img
>>>
>>> @component(slots=("icon", "message"), default="message")
... def my_message(slots):
...     with div["my-message"] as elem:
...         if slots.is_filled("icon"):
...             with span["icon"]:
...                 slots.slot("icon")
...         slots.slot("message")
...     return elem

As a result, the ``span`` element will only be present if the ``image`` slot
has been filled:

>>> with my_message() as comp:
...     p("the message")
<...>
>>> print(comp)
<div class="my-message">
  <p>the message</p>
</div>

>>> with my_message() as comp:
...     with comp.slot("icon"):
...         img(src="warning.png", alt="warning icon")
...     p("the message")
<...>
>>> print(comp)
<div class="my-message">
  <span class="icon"><img src="warning.png" alt="warning icon"></span>
  <p>the message</p>
</div>

Default content for slots
-------------------------

You can provide default content that will be inserted if a slot has not been
filled. To do hat, use :meth:`Slots.slot` as a context manager. Elements
created within the context will be used as the default content if the slot was
not filled. If the slot *was* filled, the elements will be ignored and the slot
content inserted in their place.

>>> @component(slots=("title", "icon"), default="title")
... def my_warning(slots):
...     with div["my-warning"] as elem:
...         with slots.slot("icon"):
...             img(src="warning.png", alt="warning icon")
...         with slots.slot("title"):
...             h4("Warning")
...     return elem

>>> comp = my_warning()
>>> print(comp)
<div class="my-warning">
  <img src="warning.png" alt="warning icon">
  <h4>Warning</h4>
</div>

>>> with my_warning() as comp:
...     with comp.slot("icon"):
...         img(src="error.png", alt="error icon")
...     h4("Error")
<...>
>>> print(comp)
<div class="my-warning">
  <img src="error.png" alt="error icon">
  <h4>Error</h4>
</div>

.. _component_resources:

Component styles and scripts
----------------------------

A component can define style and/or script resources that should be included in
the page where a component is used. This only has an effect when the component
is used inside a :ref:`template <templates>`.

To associate a style with a component, pass an element or list of elements to
the ``style`` parameter of the :deco:`component` decorator. Typically, this
will be one or more ``style`` or ``link`` elements. For scripts, use the
``script`` parameter.

>>> from minihtml.tags import link, script, style
>>>
>>> @component(
...     style=[
...         style(".my-component { background #ccc }"),
...         link(rel="stylesheet", href="/path/to/stylesheet.css"),
...     ],
...     script=script("alert('hello, world!);")
... )
... def my_component(slots):
...     return div["my-component"]

See :ref:`collecting` for details on how to use component styles and scripts in
a template.
