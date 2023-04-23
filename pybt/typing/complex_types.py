import random
from pybt.typing.core import BaseType, GenericAlias, _type_check

""" 
This file implements any, list and dict types for PyBT 
"""


class Any(BaseType):
    ...


class List(BaseType):
    max_len: int = 100
    sub_type: BaseType | GenericAlias = Any

    def __init__(self):
        super().__init__()

    def generate(self) -> list:
        # def _get_next():
        #     if len(self.sub_type) > 1:
        #         return random.randint(self.sub_type[0, len(self.sub_type) - 1])
        #     else:
        #         return self.sub_type[0]

        # # act according to the subtypes
        # list_gen = []
        # for _ in range(random.randint(0, self.max_len)):
        #     t = _get_next()
        #     list_gen.append(t.generate(t))
        # return list_gen
        ...

    def __str__(self):
        return "pybt.types.List"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: List[sub_type, max_length]")

        if len(parameters) == 2:
            _type_check(
                parameters,
                (
                    type,
                    int,
                ),
                "Expected types and 1 int: List[sub_type, max_length]",
            )
            cls.sub_type = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            _type_check(
                parameters, (GenericAlias,), "Expected PyBT type: List[sub_type]"
            )
            cls.sub_type = parameters[0]

        if cls.max_len < 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than 0")

        if not cls.sub_type:
            cls.sub_type = [Any]

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.sub_type = cls.sub_type
        ga.max_len = cls.max_len
        return ga


class Dict(BaseType):
    key_type: BaseType | GenericAlias = Any
    arg_type: BaseType | GenericAlias = Any

    def __init__(self):
        super().__init__()

    def generate(self) -> dict:
        ...

    def __str__(self):
        return "pybt.types.Dict"

    def __class_getitem__(cls, parameters):
        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Dict[key_type, arg_type]")

        if len(parameters) == 2:
            _type_check(
                parameters,
                (type, type),
                "Expected type and type: Dict[key_type, arg_type]",
            )
            cls.sub_type = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            _type_check(parameters, (BaseType,), "Expected PyBT type: Dict[sub_type]")
            cls.sub_type = parameters[0]

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.key_type = cls.key_type
        ga.arg_type = cls.arg_type
        return ga
