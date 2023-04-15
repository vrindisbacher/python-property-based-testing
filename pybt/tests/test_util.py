import random
from typing import _UnionGenericAlias
from types import UnionType

from pybt.core.util import _gen_complex_type_helper


BASE_TYPES = [int, float, str, bool]
COMPLEX_TYPES = [list, dict]
ALL_TYPES = BASE_TYPES + COMPLEX_TYPES


def gen_complex_type(max_depth):
    prim_type = COMPLEX_TYPES[random.randint(0, len(COMPLEX_TYPES) - 1)]
    return _gen_complex_type_helper(prim_type, max_depth, 0)
