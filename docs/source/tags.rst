.. currentmodule:: minihtml.tags

.. _tags:

Tags
====

The :mod:`minihtml.tags` module contains prototypes for the HTML elements
defined by `the HTML5 specification <https://html.spec.whatwg.org/>`_.

Tags with the same name as a python builtin, such as :data:`input` or
:data:`object`, or functions in the ``minihtml`` namespace (:data:`template`)
are available under their regular names as well as an alias with a trailing
underscore (:data:`input_`, :data:`object_`, :data:`template_`, etc.).

The ``del`` tag is available as :data:`del_` since it is the name of a Python keyword.

.. note::

   Importing ``*`` will only import non-conflicting versions of these tags::

        from minihtml.tags import *
        input_()

   To use their regular names, you have to import them directly, for example::

        from minihtml.tags import input  # masks the `input` builtin
        input()

   or access them via the module::

        import minihtml.tags as t
        t.input()

.. automodule:: minihtml.tags
   :members:
   :ignore-module-all:
