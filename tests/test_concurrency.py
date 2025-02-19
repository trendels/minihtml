import asyncio
from textwrap import dedent

from minihtml import make_prototype
from minihtml._core import Element

div = make_prototype("div")


async def test_concurrent_templates():
    async def template(name: str) -> Element:
        with div[name] as result:
            div(f"{name}-1")
            await asyncio.sleep(0.1)
            div(f"{name}-2")
        return result

    async with asyncio.TaskGroup() as tg:
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
