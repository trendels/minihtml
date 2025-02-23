.. currentmodule:: minihtml

.. _context:

Context
=======

A context is a way to make global data available everywhere inside a template
without passing it around explicitly.

Behind the scenes, a ``ContextVar`` is used to store the data. The class-based
interface is easy to use, while allowing type-checkers to know the type of data
that is being accessed.

Basic Usage
-----------

To use a context, you create a of the :class:`Context` class. The Base class
provides one classmethod, :meth:`Context.get` and implements the context
manager interface.

Typically, you will make your subclass a dataclass, but it is not required.

To set up the context, create an instance of the class and use it as a context
manager. Within the body of the context manager, the instance you created can
be received by calling the :meth:`Context.get` method of the class:

>>> from dataclasses import dataclass
>>> from minihtml import Context
>>>
>>> @dataclass
... class MyContext(Context):
...     theme: str = "light"
...
>>> def get_theme():
...     return MyContext.get().theme
...
>>> with MyContext(theme="dark"):
...     print(f"The theme is {get_theme()}.")
...     with MyContext(theme="light"):
...         print(f"The theme is now {get_theme()}.")
The theme is dark.
The theme is now light.


Use cases
---------

Context data is useful for passing around that you might need in many places in
your template. For example things like the current user's preferred language.

A context is also useful to pass around request-scoped objects. For example, a
web framework might provide a request object with an ``url_for`` method that is
used to build URLs at runtime. Instead of passing the request object to every
helper function and component in your template, you can set up a context object
once and then provide a small wrapper function that retrieves the request from
the context and calls it's `url_for` method:

.. code-block:: python

    from dataclasses import dataclass
    from my_hypothetical_framework import Request
    from minihtml import Context

    @dataclass
    class RequestContext(Context):
        request: Request

    def url_for(*args, **kwargs):
        return RequestContext.get().request.url_for(*args, **kwargs)

    @template()
    def my_template():
        return p(f"The home page is at {url_for('home')}")

    t = my_template()
    # Note that because templates are rendered lazily, it is sufficient
    # to set up the context object before calling t.render().
    with RequestContext(request=Request(base_url="http://localhost:8000/", ...)):
        print(t.render())
    # Example output:
    #   The home page is at http://localhost:8000/home

