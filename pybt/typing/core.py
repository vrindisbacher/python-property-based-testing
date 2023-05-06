from types import UnionType
import typing as PythonTyping
import random
import string

from pybt.core.exception import MistypedSignature

_DEFAULT_MAX_DEPTH = 2
_DEFAULT_MAX_LEN = 10
_DEFAULT_SUB_TYPE = None


_DEFAULT_MIN = -1000
_DEFAULT_MAX = 1000
_DEFAULT_MAX_LEN = 10


def _ensure_annot_is_pybt_type(key: str, annot: UnionType):
    """
    Inspects the types that have been unioned together to ensure that they are valid

    parameter annot: The union type annotation
    returns : A boolean indicating whether the typing is valid or not
    """
    sub_types = PythonTyping.get_args(annot)
    for type in sub_types:
        if not (_try_attr(type, "_pybt_type") or _try_attr(type, "_alias")):
            raise MistypedSignature(
                f"""
                {key} was given subtype with type {type} which is not a PyBT type. 
                Please use a PyBT type. 
                """
            )


def _try_attr(obj, name):
    try:
        getattr(obj, name)
        return True
    except AttributeError:
        return False


def _flat_union(t: type) -> list:
    base_type = PythonTyping.get_origin(t)
    sub_type = PythonTyping.get_args(t)
    if not base_type:
        return [t]
    else:
        return sub_type


def _get_next(choices):
    if not choices or not len(choices):
        choice = _NoneGenericAlias
    elif len(choices) > 1:
        choice = choices[random.randint(0, len(choices) - 1)]
    else:
        choice = choices[0]

    if _try_attr(choice, "_alias"):
        return choice._alias()
    elif type(choice) == type:
        return choice()
    else:
        return choice


class BaseType:
    def __init__(self):
        raise TypeError(f"{self} object is not instantiable")

    def __call__(self, *args, **kwds):
        raise TypeError(f"{self} object is not instantiable")

    @classmethod
    def generate(cls):
        return cls._alias().generate()


class GenericBase:
    _pybt_type = True

    def __or__(self, other):
        return PythonTyping.Union[self, other]

    def __ror__(self, other):
        return PythonTyping.Union[self, other]


class _NoneGenericAlias(GenericBase):
    def __init__(self):
        ...

    def generate(self) -> None:
        return None


class _BoolGenericAlias(GenericBase):
    def __init__(self):
        ...

    def generate(self) -> bool:
        return [True, False][random.randint(0, 1)]


class _IntGenericAlias(GenericBase):
    def __init__(self, min=_DEFAULT_MIN, max=_DEFAULT_MAX):
        self.min: int = _DEFAULT_MIN
        self.max: int = _DEFAULT_MAX
        if min is not None:
            self.min = min
        if max is not None:
            self.max = max

    def generate(self) -> int:
        return random.randint(self.min, self.max)


class _FloatGenericAlias(GenericBase):
    def __init__(self, min=_DEFAULT_MIN, max=_DEFAULT_MAX):
        self.min: float = _DEFAULT_MIN
        self.max: float = _DEFAULT_MAX
        if min is not None:
            self.min = min
        if max is not None:
            self.max = max

    def generate(self) -> float:
        return random.random() * random.randint(self.min, self.max)


class _StringGenericAlias(GenericBase):
    def __init__(self, max_len=_DEFAULT_MAX_LEN):
        self.max_len: int = _DEFAULT_MAX_LEN
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> str:
        return "".join(
            random.choices(string.ascii_letters, k=random.randint(1, self.max_len))
        )


class _UnionGenericAlias(GenericBase):
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE):
        self.sub_type = sub_type
        _ensure_annot_is_pybt_type("Union", self.sub_type)

    def generate(self) -> any:
        if not self.sub_type:
            sub_type_choices = [_AnyGenericAlias]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        choice = _get_next(sub_type_choices)

        return choice.generate()


class _AnyGenericAlias(GenericBase):
    def __init__(self, max_depth=_DEFAULT_MAX_DEPTH, max_len=_DEFAULT_MAX_LEN):
        self.max_depth: int = _DEFAULT_MAX_DEPTH
        self.max_len: int = _DEFAULT_MAX_LEN
        if max_depth is not None:
            self.max_depth = max_depth
        if max_len is not None:
            self.max_len = max_len

    def create_any(self, base_type, times_called):
        if type(base_type) == _SetGenericAlias:
            _all_types = [
                _IntGenericAlias,
                _StringGenericAlias,
                _BoolGenericAlias,
                _FloatGenericAlias,
                _NoneGenericAlias,
            ]
            _base_types = [
                _IntGenericAlias,
                _StringGenericAlias,
                _BoolGenericAlias,
                _FloatGenericAlias,
                _NoneGenericAlias,
            ]
        else:
            _all_types = [
                _ListGenericAlias,
                _TupleGenericAlias,
                _DictGenericAlias,
                _SetGenericAlias,
                _IntGenericAlias,
                _StringGenericAlias,
                _BoolGenericAlias,
                _FloatGenericAlias,
                _NoneGenericAlias,
            ]
            _base_types = [
                _IntGenericAlias,
                _StringGenericAlias,
                _BoolGenericAlias,
                _FloatGenericAlias,
                _NoneGenericAlias,
            ]
        types = []
        for _ in range(self.max_len):
            next = _all_types[random.randint(0, len(_all_types) - 1)]()
            if type(next) not in _base_types:
                if times_called <= self.max_depth:
                    types.append(self.create_any(next, times_called + 1))
            else:
                types.append(next)

        sub_types = PythonTyping._UnionGenericAlias(UnionType, tuple(types))

        if isinstance(base_type, _DictGenericAlias):
            key_type = _base_types[random.randint(0, len(_base_types) - 1)]()
            base_type.key_type = key_type
            base_type.arg_type = sub_types
            return base_type

        base_type.sub_type = sub_types
        return base_type

    def generate(self) -> any:
        _ALL_TYPES: list = [
            _ListGenericAlias,
            _TupleGenericAlias,
            _DictGenericAlias,
            _IntGenericAlias,
            _StringGenericAlias,
            _BoolGenericAlias,
            _FloatGenericAlias,
            _NoneGenericAlias,
        ]
        _BASE_TYPES: list = [
            _IntGenericAlias,
            _StringGenericAlias,
            _BoolGenericAlias,
            _FloatGenericAlias,
            _NoneGenericAlias,
        ]
        base_type = _ALL_TYPES[random.randint(0, len(_ALL_TYPES) - 1)]()

        if type(base_type) in _BASE_TYPES:
            return base_type.generate()

        type_to_gen = self.create_any(base_type, 0)
        return type_to_gen.generate()


class _ListGenericAlias(GenericBase):
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE, max_len=_DEFAULT_MAX_LEN):
        self.max_len: int = _DEFAULT_MAX_LEN
        self.sub_type = sub_type
        _ensure_annot_is_pybt_type("List", self.sub_type)
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> list:
        if not self.sub_type:
            sub_type_choices = [_AnyGenericAlias]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        list_gen = []
        for _ in range(random.randint(0, self.max_len)):
            t = _get_next(sub_type_choices)
            list_gen.append(t.generate())
        return list_gen


class _TupleGenericAlias(GenericBase):
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE, max_len=_DEFAULT_MAX_LEN):
        self.max_len = _DEFAULT_MAX_LEN
        self.sub_type = sub_type
        _ensure_annot_is_pybt_type("Tuple", self.sub_type)
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> tuple:
        list_type = _ListGenericAlias(self.sub_type, self.max_len)
        return tuple(list_type.generate())


class _SetGenericAlias(GenericBase):
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE, max_len=_DEFAULT_MAX_LEN):
        self.max_len = _DEFAULT_MAX_LEN
        self.sub_type = sub_type
        _ensure_annot_is_pybt_type("Set", self.sub_type)
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> set:
        if self.sub_type is None:
            self.sub_type = (
                _IntGenericAlias()
                | _StringGenericAlias()
                | _BoolGenericAlias()
                | _FloatGenericAlias()
                | _TupleGenericAlias(
                    _IntGenericAlias()
                    | _StringGenericAlias()
                    | _BoolGenericAlias()
                    | _BoolGenericAlias()
                )
            )
        list_type = _ListGenericAlias(self.sub_type, self.max_len)
        return set(list_type.generate())


class _DictGenericAlias(GenericBase):
    def __init__(
        self,
        key_type=_DEFAULT_SUB_TYPE,
        arg_type=_DEFAULT_SUB_TYPE,
        max_keys=_DEFAULT_MAX_LEN,
    ):
        self.max_keys: int = _DEFAULT_MAX_LEN
        self.key_type = key_type
        _ensure_annot_is_pybt_type("Dictionary Key", self.key_type)
        self.arg_type = arg_type
        _ensure_annot_is_pybt_type("Dictionary Args", self.arg_type)
        if max_keys is not None:
            self.max_keys = max_keys

    def generate(self) -> dict:
        if not self.key_type:
            key_type_choices = [
                _IntGenericAlias,
                _FloatGenericAlias,
                _BoolGenericAlias,
                _StringGenericAlias,
            ]
        else:
            key_type_choices = _flat_union(self.key_type)

        if not self.arg_type:
            arg_type_choices = [_AnyGenericAlias]
        else:
            arg_type_choices = _flat_union(self.arg_type)

        dict_gen = {}
        for _ in range(random.randint(0, self.max_keys)):
            key = _get_next(key_type_choices)
            arg = _get_next(arg_type_choices)
            dict_gen[key.generate()] = arg.generate()
        return dict_gen


class _FunctionGenericAlias(GenericBase):
    def __init__(self, return_type=None):
        self.return_type = return_type
        _ensure_annot_is_pybt_type("Function", self.return_type)

    def generate(self):
        if not self.return_type:
            sub_type_choices = [_AnyGenericAlias()]
        else:
            sub_type_choices = _flat_union(self.return_type)

        t = _get_next(sub_type_choices)
        return lambda *x: t.generate()
