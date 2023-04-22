import random
import string
import typing

from typing import _UnionGenericAlias
from types import UnionType

from pybt.core.exception import MutableTypeAsDict


BASE_TYPES = [int, float, str, bool, None]
COMPLEX_TYPES = [list, dict]
ALL_TYPES = BASE_TYPES + COMPLEX_TYPES

# generators


def gen_int(max_basic_arg_size: int) -> int:
    """
    Generates a random integer

    parameter max_basic_arg_size : the max size for basic datatypes

    returns : an integer
    """
    return random.randrange(-1 * max_basic_arg_size - 1, max_basic_arg_size)


def gen_float(max_basic_arg_size: int) -> float:
    """
    Generates a random float

    parameter max_basic_arg_size : the max size for basic datatypes

    returns : a float
    """
    return random.random() * gen_int(max_basic_arg_size)


def gen_str(max_basic_arg_size: int) -> str:
    """
    Generates a random string

    parameter max_basic_arg_size : the max size for basic datatypes

    returns : a string
    """
    return "".join(
        random.choices(string.ascii_letters, k=random.randint(1, max_basic_arg_size))
    )


def gen_bool() -> bool:
    """
    Generates a random bool

    parameter max_basic_arg_size : the max size for basic datatypes

    returns : a bool
    """
    return [True, False][random.randint(0, 1)]


def gen_list(max_complex_arg_size, type_gen_list):
    """
    Generates a random list based on the function provided in type_gen_list

    parameter max_complex_arg_size : the max size for complex datatypes
    parameter type_gen_list : the function (generator) for the list to build

    returns : a list in accordance with type_gen_list
    """
    built_list = []
    for _ in range(random.randint(0, max_complex_arg_size)):
        next = type_gen_list[random.randint(0, len(type_gen_list) - 1)]
        if type(next) is list:
            built_list.append(next[random.randint(0, len(next) - 1)]())
        else:
            built_list.append(next())
    return built_list


def gen_dict(max_complex_arg_size, type_gen_dict):
    """
    Generates a random dict based on the function provided in type_gen_dict

    parameter max_complex_arg_size : the max size for complex datatypes
    parameter type_gen_dict : the function (generator) for the dict to build

    returns : a dict in accordance with type_gen_dict
    """
    d = {}
    key = type_gen_dict[0]  # the key is always 0
    sub_gen = type_gen_dict[1]  # the types are always 1
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
            raise MutableTypeAsDict(
                """
                Mutable types cannot be dictionary keys. 
                Please fix your type annotations.
                """
            )

        if type(next) is list:
            d[key_to_use] = next[random.randint(0, len(next) - 1)]()
        else:
            d[key_to_use] = next()

    return d


def _gen_complex_type_helper(prim_type, max_len_and_depth, num_calls):
    """
    Generates a random type with a max_depth.

    parameter prim_type : the base type to use - a complex type (either list or dict)
    parameter max_len_and_depth : the most nested types possible, and the longest sequence of
                                  union types for the random type
    parameter num_calls : The number of calls we have made to _gen_complex_type_helper.

    returns : A complex type with a bunch of sub types
    """
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
    """
    Generates a random type with a max_depth.

    parameter max_depth : the most nested types possible for the random type
    parameter base_type : Default to None. If provided, it will be used as the
                          base for a series of subtypes (if it is a list or dict),
                          otherwise (if it is a base type) it will be returned.

    returns : a type that is either a basic type, or a complex type with a bunch of sub types
    """
    if not base_type:
        base_type = ALL_TYPES[random.randint(0, len(ALL_TYPES) - 1)]

    if base_type in COMPLEX_TYPES:
        return _gen_complex_type_helper(base_type, max_depth, 0)

    return base_type


def gen_callable(ret_gen):
    """
    Generates a random return value of proper type for a function

    parameter max_complex_arg_size : the max size for complex datatypes
    parameter ret_gen : the function (generator) for the callable to return

    returns : a return type in accordance with ret_gen
    """
    if type(ret_gen[0]) == list:
        return lambda *x: ret_gen[0][0]()
    return lambda *x: ret_gen[0]()


def get_base_type() -> int | str | bool | float:
    """
    Generates a base type.

    returns : an int, str, bool, or float
    """
    return BASE_TYPES[random.randint(0, len(BASE_TYPES) - 1)]


# other utilities


def is_base_type(obj: type) -> bool:
    """
    Check whether the provided type (obj) is a base type

    returns : a boolean indicating whether the provided type is a base type
    """
    return typing.get_origin(obj) is None and obj in BASE_TYPES + [any]
