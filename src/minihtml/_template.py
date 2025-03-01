import io
from collections.abc import Iterable
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, TextIO, TypeAlias, overload

from ._component import Component, ComponentWrapper
from ._core import HasNodes, Node, iter_nodes, register_with_context
from ._template_context import get_template_context, template_context

P = ParamSpec("P")

TemplateImpl: TypeAlias = Callable[P, Node | HasNodes]
TemplateImplLayout: TypeAlias = Callable[Concatenate[Component, P], None]


class Template:
    def __init__(self, callback: Callable[[], list[Node]]):
        self._callback = callback

    def render(self, *, doctype: bool = True) -> str:
        nodes = self._callback()
        buf = io.StringIO()
        if doctype:
            buf.write("<!doctype html>\n")
        Node.render_list(buf, nodes)
        buf.write("\n")
        return buf.getvalue()


@overload
def template() -> Callable[[TemplateImpl[P]], Callable[P, Template]]: ...


@overload
def template(
    *, layout: ComponentWrapper[...]
) -> Callable[[TemplateImplLayout[P]], Callable[P, Template]]: ...


def template(
    *, layout: ComponentWrapper[...] | None = None
) -> (
    Callable[[TemplateImpl[P]], Callable[P, Template]]
    | Callable[[TemplateImplLayout[P]], Callable[P, Template]]
):
    if layout is None:

        def plain_decorator(fn: TemplateImpl[P]) -> Callable[P, Template]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Template:
                def callback() -> list[Node]:
                    with template_context():
                        result = fn(*args, **kwargs)
                        return list(iter_nodes([result]))

                return Template(callback)

            return wrapper

        return plain_decorator

    else:

        def layout_decorator(fn: TemplateImplLayout[P]) -> Callable[P, Template]:
            @wraps(fn)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Template:
                def callback() -> list[Node]:
                    with template_context():
                        with layout() as result:
                            fn(result, *args, **kwargs)
                        return list(iter_nodes([result]))

                return Template(callback)

            return wrapper

        return layout_decorator


class ResourceWrapper(Node):
    def __init__(self, nodes: Iterable[Node]):
        self._nodes = nodes
        self._inline = False

    def write(self, f: TextIO, indent: int = 0) -> None:
        nodes = list(self._nodes)
        n = len(nodes)
        for i, node in enumerate(nodes):
            node.write(f, indent)
            if i < n - 1:
                f.write("\n")
                f.write("  " * indent)


def component_styles() -> ResourceWrapper:
    """
    Placeholder element for component styles.

    Can only be used in code called from a :deco:`template`. Inserts the style
    nodes collected from all components used in the current template.
    """
    wrapper = ResourceWrapper(get_template_context().styles)
    register_with_context(wrapper)
    return wrapper


def component_scripts() -> ResourceWrapper:
    """
    Placeholder element for component scripts.

    Can only be used in code called from a :deco:`template`. Inserts the script
    nodes collected from all components used in the current template.
    """
    wrapper = ResourceWrapper(get_template_context().scripts)
    register_with_context(wrapper)
    return wrapper
