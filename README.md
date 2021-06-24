# Simple HTML generation

[![PyPI](https://img.shields.io/pypi/v/minihtml)](https://pypi.python.org/pypi/minihtml)

## Installation

Install the `minihtml` package from PyPI:

    $ pip install minihtml

## Examples

Create a `minihtml.Html` instance to produce tags. Tags stringify to HTML:

~~~python
>>> from minihtml import Html
>>> h = Html()
>>> html = h.html(h.head(h.title("Hello, World!")))
>>> print(html)
<html><head><title>Hello, World!</title></head></html>

~~~

Tags are callables that accept positional arguments (children) and keyword
arguments (attributes). Calls can be chained to produce code that is structured
more like HTML (attributes before content):

~~~python
>>> print(h.a("link title", href="/url"))
<a href="/url">link title</a>
>>> print(h.a(href="/url")("link title"))
<a href="/url">link title</a>

~~~

There are shortcuts for setting the `class` and `id` attributes using `[]` accessors:

~~~python
>>> print(h.div["#header bg-white"](h.span["text-xl font-medium"]("hello")))
<div id="header" class="bg-white"><span class="text-xl font-medium">hello</span></div>

~~~

Text content, attribute names and attribute values are escaped automatically.
To include unescaped content, use the `raw` element. Only use this with
**trusted** input:

~~~python
>>> print(h.div(foo='"bar"')("2 > 1"))
<div foo="&quot;bar&quot;">2 &gt; 1</div>
>>> print(h.script(h.raw('if (2 > 1) console.log("math still works");')))
<script>if (2 > 1) console.log("math still works");</script>

~~~

To use tag or attribute names that conflict with python keywords, append an
underscore. Underscores within attribute names are converted to hyphens ("-",
except for a single underscore, which is passed through unchanged).

~~~python
>>> print(h.del_("deleted text"))
<del>deleted text</del>
>>> print(h.label(for_="fieldname")("text"))
<label for="fieldname">text</label>
>>> print(h.span(data_foo="bar"))
<span data-foo="bar"></span>
>>> print(h.span(_="something"))
<span _="something"></span>

~~~

Attributes that have no value can be set by passing the value `True`:

~~~python
>>> print(h.input(type="text", disabled=True))
<input type="text" disabled />

~~~

Use `minihtml.tostring` to convert a tag to a string and add a doctype:

~~~python
>>> from minihtml import tostring
>>> html = h.html(h.body("my website"))
>>> tostring(html)
'<!doctype html>\n<html><body>my website</body></html>\n'

~~~

## License

minihtml is licensed under the MIT license. See the included file `LICENSE`
for details.
