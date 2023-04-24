from pybt.core import pybt
from pybt.typing.basic_types import NoneType, Int, Str
from pybt.typing.complex_types import List, Dict
from typing import Union

@pybt
def test_handles_none_with_arged_types(
    x: Union[Int[0, 10], List[Int], Str, Dict[NoneType, List[NoneType]]]
):
    assert type(x) in [int, list, str, dict, list]
    if type(x) == int:
        assert x >= 0 and x <= 10
    if type(x) == list:
        assert all([el is None for el in x])
    if type(x) == dict:
        for k, v in x.items():
            assert k is None
            assert type(v) == list
            for el in v:
                assert el is None
