import random
from typing import _UnionGenericAlias
from types import UnionType


BASE_TYPES = [int, float, str, bool]
COMPLEX_TYPES = [list, dict]
ALL_TYPES = BASE_TYPES + COMPLEX_TYPES


def _gen_complex_type_helper(prim_type, max_len_and_depth, num_calls):
    list_of_types = []
    for _ in range(max_len_and_depth):
        if num_calls <= max_len_and_depth:
            next_type = ALL_TYPES[random.randint(0, len(ALL_TYPES) - 1)]
        else:
            next_type = BASE_TYPES[random.randint(0, len(BASE_TYPES) - 1)]

        if next_type in COMPLEX_TYPES:
            list_of_types.append(_gen_complex_type_helper(next_type, max_len_and_depth, num_calls + 1))
        else:
            list_of_types.append(next_type)
    
    # some magix to generate union types dynamically 
    sub_types = _UnionGenericAlias(UnionType, tuple(list_of_types))

    return prim_type[sub_types]


def gen_complex_type(max_depth):
    prim_type = COMPLEX_TYPES[random.randint(0, len(COMPLEX_TYPES) - 1)]
    return _gen_complex_type_helper(prim_type, max_depth, 0)