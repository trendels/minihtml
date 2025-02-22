import asyncio
import sys
from textwrap import dedent

if sys.version_info >= (3, 11):
    from asyncio import TaskGroup
else:
    from taskgroup import TaskGroup

from minihtml import Element, make_prototype

div = make_prototype("div")


async def test_concurrent_templates():
    async def template(name: str) -> Element:
        with div[name] as result:
            div(f"{name}-1")
            await asyncio.sleep(0.1)
            div(f"{name}-2")
        return result

    async with TaskGroup() as tg:
        t1 = tg.create_task(template("a"))
        t2 = tg.create_task(template("b"))

    e1 = t1.result()
    e2 = t2.result()

    assert str(e1) == dedent("""\
        <div class="a">
          <div>a-1</div>
          <div>a-2</div>
        </div>""")

    assert str(e2) == dedent("""\
        <div class="b">
          <div>b-1</div>
          <div>b-2</div>
        </div>""")
