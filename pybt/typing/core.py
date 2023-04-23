def _type_check(args, types, msg):
    for idx, el in enumerate(args):
        if type(el) != types[idx]:
            raise TypeError(msg)


class GenericAlias:
    def __init__(self, origin, parameters, generator):
        self.origin = origin
        self.parameters = parameters
        self.generate = generator

    def __mro_entries__(self, bases):
        return (self.origin,)


class BaseType:
    def __call__(self, *args, **kwds):
        raise TypeError("Cannot instantiate type {self}")

    def generate(self):
        raise NotImplementedError("Generator for {self} not implemented!")
