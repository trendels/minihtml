from dataclasses import dataclass

from pytest import raises as assert_raises

from minihtml import Context


@dataclass
class MyContext(Context):
    name: str


@dataclass
class OtherContext(Context):
    port: int


def test_set_and_get_context():
    g = MyContext(name="fred")
    with g:
        assert MyContext.get() is g


def test_multiple_context_objects_coexist():
    with MyContext(name="barney"), OtherContext(port=80):
        assert MyContext.get().name == "barney"
        assert OtherContext.get().port == 80


def test_set_replaces_previous_value():
    with MyContext(name="barney"), MyContext(name="wilma"):
        assert MyContext.get().name == "wilma"


def test_value_is_unset_when_leaving_context_manager():
    with OtherContext(port=80):
        with MyContext(name="barney"):
            pass

        with assert_raises(LookupError):
            MyContext.get()

        assert OtherContext.get().port == 80


def test_can_nest_context_managers():
    with MyContext(name="fred"):
        assert MyContext.get().name == "fred"

        with MyContext(name="barney"):
            assert MyContext.get().name == "barney"

        assert MyContext.get().name == "fred"
