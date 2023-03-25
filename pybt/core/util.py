import random
import string
import typing


# generators


def gen_int(max_basic_arg_size):
    return random.randrange(-1 * max_basic_arg_size - 1, max_basic_arg_size)


def gen_float():
    return random.random() * gen_int()


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
    type_gen_list = type_gen_list[1]  # the types are always 1

    for _ in range(random.randint(0, max_complex_arg_size)):
        if type(type_gen_list) is list:
            next = type_gen_list[random.randint(0, len(type_gen_list) - 1)]
        else:
            next = type_gen_list

        if type(key) is list:
            key_to_use = key[random.randint(0, len(key) - 1)]()
        else:
            key_to_use = key()

        if type(next) is list:
            d[key_to_use] = next[random.randint(0, len(next) - 1)]()
        else:
            d[key_to_use] = next()

    return d


# other utilities


def is_base_type(obj):
    return typing.get_origin(obj) is None  
