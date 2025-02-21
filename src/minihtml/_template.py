import io
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TypeAlias, overload

from ._component import Component
from ._core import HasNodes, Node, iter_nodes

P = ParamSpec("P")

TemplateImpl: TypeAlias = Callable[P, Node | HasNodes]
TemplateImplLayout: TypeAlias = Callable[Concatenate[Component, P], None]


def _render(result: Node | HasNodes, doctype: bool) -> str:
    buf = io.StringIO()
    if doctype:
        buf.write("<!doctype html>\n")
    Node.render_list(buf, iter_nodes([result]))
    buf.write("\n")
    return buf.getvalue()


@overload
def template(
    *, doctype: bool = ...
) -> Callable[[TemplateImpl[P]], Callable[P, str]]: ...


@overload
def template(
    layout: Component, *, doctype: bool = ...
) -> Callable[[TemplateImplLayout[P]], Callable[P, str]]: ...


def template(
    layout: Component | None = None,
    *,
    doctype: bool = True,
) -> (
    Callable[[TemplateImpl[P]], Callable[P, str]]
    | Callable[[TemplateImplLayout[P]], Callable[P, str]]
):
    if layout is None:

        def plain_decorator(fn: TemplateImpl[P]) -> Callable[P, str]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
                result = fn(*args, **kwargs)
                return _render(result, doctype=doctype)

            return wrapper

        return plain_decorator

    else:

        def layout_decorator(fn: TemplateImplLayout[P]) -> Callable[P, str]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
                with layout as result:
                    fn(layout, *args, **kwargs)
                return _render(result, doctype=doctype)

            return wrapper

        return layout_decorator
