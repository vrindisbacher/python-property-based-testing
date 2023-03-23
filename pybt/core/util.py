import random
import string
import typing


MAX_INT = 100000
MIN_INT = -1 * MAX_INT - 1

# generators


def gen_int():
    return random.randrange(0, MAX_INT)


def gen_float():
    return random.random() * gen_int()


def gen_str():
    return "".join(random.choices(string.ascii_letters, k=random.randint(1, 100)))


def gen_bool():
    return [True, False][random.randint(0, 1)]


def gen_list(type_gen_list):
    l = []
    rot = 0
    for _ in range(random.randint(1, 100)):
        rot %= len(type_gen_list)
        print(rot)
        type_gen = type_gen_list[rot]
        l.append(type_gen())
        rot += 1
    return l


# other utilities


def is_base_type(obj):
    return len(typing.get_args(obj)) == 0
