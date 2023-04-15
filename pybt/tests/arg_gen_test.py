from functools import partial
import typing

from pybt.core.core import DATA_STRUCT_TYPE_MAP, BASIC_TYPE_MAP, _get_complex_args, pybt
from pybt.tests.test_util import gen_complex_type


MAX_TYPE_LEN = 5

# these are irrelevant but need to set them in _get_complex_args
max_basic_type_size = 1
max_complex_type_size = 1

generators = {"t": lambda: gen_complex_type(MAX_TYPE_LEN)}
type_pybt = pybt(generators=generators, n=10000)


def find_func_for_type(t):
    if t in DATA_STRUCT_TYPE_MAP.keys():
        return DATA_STRUCT_TYPE_MAP[t](max_complex_type_size, [])
    elif t in BASIC_TYPE_MAP.keys():
        return BASIC_TYPE_MAP[t](max_complex_type_size)

    raise Exception("Failed to find function")


def complex_arg_gen_prop(t, f):
    # it should always be a function that corresponds to the base type

    base = typing.get_origin(t)
    sub_types = typing.get_args(t)

    if base:
        assert find_func_for_type(base).func == f.func
        # complex type - so look at sub_types
        idx = 0
        for arg in f.args:
            if type(arg) is list:
                idx_ = 0
                for arg_ in arg:
                    new_f = arg_[idx] if type(arg_) is list else arg_
                    complex_arg_gen_prop(typing.get_args(sub_types[idx])[idx_], new_f)
                    idx_ += 1
                idx += 1
    else:
        if type(f) is partial:
            assert find_func_for_type(t).func == f.func
        else:
            assert find_func_for_type(t) == f


@type_pybt
def test_complex_args_with_pybt(t: type):
    f = _get_complex_args(t, max_basic_type_size, max_complex_type_size)
    complex_arg_gen_prop(t, f)


test_complex_args_with_pybt()
