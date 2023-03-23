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
    for _ in range(random.randint(0, 100)):
        next = type_gen_list[random.randint(0, len(type_gen_list) - 1)]
        if type(next) is list:
            l.append(next[random.randint(0, len(next) - 1)]())
        else:
            l.append(next())
    return l


def gen_dict(type_gen_list):
    d = {}

    key = type_gen_list[0]  # the key is always 0
    type_gen_list = type_gen_list[1]  # the types are always 1

    for _ in range(random.randint(0, 100)):
        if type(type_gen_list) is list: 
            next = type_gen_list[random.randint(0, len(type_gen_list) - 1)]
        else:
            next = type_gen_list

        if type(key) is list:
            key_to_use = key[random.randint(0, len(key) - 1)]()
        else:
            key_to_use = key()

        if type(next) is list:
            # need to not get the zero'th element
            d[key_to_use] = next[random.randint(0, len(next) - 1)]()
        else:
            d[key_to_use] = next()

    return d


# other utilities


def is_base_type(obj):
    return len(typing.get_args(obj)) == 0
