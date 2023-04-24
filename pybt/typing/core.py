import typing as PythonTyping


def _type_check(args, types, msg):
    for idx, el in enumerate(args):
        if type(el) != types[idx]:
            raise TypeError(msg)


def _flat_union(t: type) -> list:
    base_type = PythonTyping.get_origin(t)
    sub_type = PythonTyping.get_args(t)
    if not base_type:
        return [t]
    else:
        return sub_type
