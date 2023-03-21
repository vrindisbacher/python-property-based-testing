import random
import string
import typing


MAX_INT = 100000

# generators


def gen_int():
    return random.randrange(0, MAX_INT)


def gen_float():
    return random.random() * gen_int()


def gen_str():
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 100)))


def gen_bool():
    return [True, False][random.randint(0, 1)]


# other utilities


def is_base_type(obj):
    return len(typing.get_args(obj)) == 0
