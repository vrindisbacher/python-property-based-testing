import random
import string
import typing

import random
from typing import _UnionGenericAlias
from types import UnionType


BASE_TYPES = [int, float, str, bool]
COMPLEX_TYPES = [list, dict]
ALL_TYPES = BASE_TYPES + COMPLEX_TYPES

# generators


def gen_int(max_basic_arg_size):
    return random.randrange(-1 * max_basic_arg_size - 1, max_basic_arg_size)


def gen_float(max_basic_arg_size):
    return random.random() * gen_int(max_basic_arg_size)


def gen_str(max_basic_arg_size):
    return "".join(
        random.choices(string.ascii_letters, k=random.randint(1, max_basic_arg_size))
    )


def gen_bool():
    return [True, False][random.randint(0, 1)]


def gen_list(max_complex_arg_size, type_gen_list):
    l = []
    for _ in range(random.randint(0, max_complex_arg_size)):
        next = type_gen_list[random.randint(0, len(type_gen_list) - 1)]
        if type(next) is list:
            l.append(next[random.randint(0, len(next) - 1)]())
        else:
            l.append(next())
    return l


def gen_dict(max_complex_arg_size, type_gen_list):
    d = {}
    key = type_gen_list[0]  # the key is always 0
    sub_gen = type_gen_list[1]  # the types are always 1
    for _ in range(random.randint(0, max_complex_arg_size)):
        if type(sub_gen) is list:
            next = sub_gen[random.randint(0, len(sub_gen) - 1)]
        else:
            next = sub_gen

        if type(key) is list:
            key_to_use = key[random.randint(0, len(key) - 1)]()
        else:
            key_to_use = key()

        if type(key_to_use) in [list, dict]:
            raise Exception(
                "Mutable types cannot be dictionary keys. Please fix your type annotations"
            )

        if type(next) is list:
            d[key_to_use] = next[random.randint(0, len(next) - 1)]()
        else:
            d[key_to_use] = next()

    return d


def _gen_complex_type_helper(prim_type, max_len_and_depth, num_calls):
    list_of_types = []
    for _ in range(max_len_and_depth):
        if num_calls <= max_len_and_depth:
            next_type = ALL_TYPES[random.randint(0, len(ALL_TYPES) - 1)]
        else:
            next_type = BASE_TYPES[random.randint(0, len(BASE_TYPES) - 1)]

        if next_type in COMPLEX_TYPES:
            list_of_types.append(
                _gen_complex_type_helper(next_type, max_len_and_depth, num_calls + 1)
            )
        else:
            list_of_types.append(next_type)

    # some magic to generate union types dynamically
    sub_types = _UnionGenericAlias(UnionType, tuple(list_of_types))

    if prim_type == dict:
        key_types = BASE_TYPES[random.randint(0, len(BASE_TYPES) - 1)]
        return prim_type[key_types, sub_types]

    return prim_type[sub_types]


def gen_any(max_depth, base_type=None):
    if not base_type:
        base_type = ALL_TYPES[random.randint(0, len(ALL_TYPES) - 1)]

    if base_type in COMPLEX_TYPES:
        return _gen_complex_type_helper(base_type, max_depth, 0)

    return base_type


def get_base_type():
    return BASE_TYPES[random.randint(0, len(BASE_TYPES) - 1)]


# other utilities


def is_base_type(obj):
    return typing.get_origin(obj) is None and obj in BASE_TYPES + [any]
