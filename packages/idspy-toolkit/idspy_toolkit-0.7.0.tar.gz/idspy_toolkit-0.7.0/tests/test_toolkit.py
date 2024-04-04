import dataclasses
import numpy as np
import pytest
from idspy_toolkit.utils import snake2camel, camel2snake, get_field_with_type, extract_ndarray_info, \
    _imas_default_values, __get_field_type, get_all_class
from idspy_toolkit.accessor import get_type_arg
from idspy_toolkit.toolkit import fill_default_values_ids


@dataclasses.dataclass#(slots=True)
class child3:
    # c3:str=dataclasses.field(default_factory=lambda:"here")
    c3: str = dataclasses.field(default="nested_value")


@dataclasses.dataclass#(slots=True)
class child2:
    # c2:child3=dataclasses.field(default_factory=lambda:child3())
    # z:int=dataclasses.field(default_factory=lambda:123)
    c2: child3 = dataclasses.field(default=None)


@dataclasses.dataclass#(slots=True)
class child1:
    b: str = ""  # dataclasses.field(default_factory=lambda:"")


@dataclasses.dataclass#(slots=True)
class root:
    a: str = dataclasses.field(default="a")
    b: child1 = dataclasses.field(default=None)
    c: child2 = dataclasses.field(default=None)


def test_creation_subtype():
    ut_test = root()
    assert ut_test.c is None
    atype, _ = get_type_arg(ut_test, "c")
    assert dataclasses.is_dataclass(atype())
    fill_default_values_ids(ut_test)
    assert ut_test.c.c2 is not None
    assert ut_test.c.c2.c3 == "nested_value"
