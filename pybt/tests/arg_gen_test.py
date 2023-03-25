from functools import partial
import typing

from pybt.core.core import DATA_STRUCT_TYPE_MAP, BASIC_TYPE_MAP, _get_complex_args, pybt
from pybt.tests.test_util import gen_complex_type


MAX_TYPE_LEN = 3

# these are irrelevant but need to set them in _get_complex_args
max_basic_type_size = 1
max_complex_type_size = 1

generators = {"t": lambda: gen_complex_type(MAX_TYPE_LEN)}
type_pybt = partial(pybt, generators=generators)



def find_func_for_type(t):
    if t in DATA_STRUCT_TYPE_MAP.keys():
        return DATA_STRUCT_TYPE_MAP[t](max_complex_type_size, [])
    elif t in BASIC_TYPE_MAP:
        return DATA_STRUCT_TYPE_MAP[t](max_complex_type_size)

    raise Exception("Failed to find function")

def complex_arg_gen_prop(t, f):
    # it should always be a function that corresponds to the base type
    base = typing.get_origin(t)
    sub_types = typing.get_args(t)
        
    if base: 
        # it is a complex type - check the function is correct 
        assert(find_func_for_type(base).func == f.func)
        # do some more stuff here 
    else:
        assert(find_func_for_type(t).func == f.func)

@type_pybt
def test_complex_args_with_pybt(t: type):
    f = _get_complex_args(t, max_basic_type_size, max_complex_type_size)
    complex_arg_gen_prop(t, f)


test_complex_args_with_pybt()
