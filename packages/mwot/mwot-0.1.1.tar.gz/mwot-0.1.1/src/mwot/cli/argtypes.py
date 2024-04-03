"""Fancy argparse type conversion."""

from ..compiler import bits_from_mwot
from ..util import split

truthies = {'true', 't', 'yes', 'y', '1'}
falsies = {'false', 'f', 'no', 'n', '0'}
decomps = {'basic', 'guide', 'rand'}


class ArgType:
    """Argparse option type with a display name."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def __call__(self, val):
        """Convert a string to the correct type.

        Raises ValueError if that's not possible.
        """
        return self.function(val)

    def __repr__(self):
        return self.name


def argtype(name):
    """Turn a function into an ArgType."""

    def decorator(fn):
        return ArgType(name, fn)

    return decorator


def ArgUnion(*argtypes):
    """Create a union of arg types."""
    name = ' or '.join(i.name for i in argtypes).replace(' ', '-')

    def function(val):
        for atype in argtypes:
            try:
                return atype(val)
            except ValueError:
                pass
        raise ValueError('unknown type')

    return ArgType(name, function)


@argtype('boolean')
def BooleanArg(val):
    val = val.casefold()
    if val in truthies:
        return True
    if val in falsies:
        return False
    raise ValueError('unknown boolean keyword')


@argtype('decompiler')
def DecompilerArg(val):
    val = val.casefold()
    if val in decomps:
        return val
    raise ValueError('unknown decompiler')


@argtype('integer')
def IntArg(val):
    return int(val)


@argtype('none')
def NoneArg(val):
    val = val.casefold()
    if val != 'none':
        raise ValueError('not none')
    return None


@argtype('positive integer')
def PosIntArg(val):
    num = int(val)
    if num <= 0:
        raise ValueError('nonpositive int')
    return num


@argtype('vocab')
def VocabArg(val):
    desired = (0, 1)
    words = tuple(split(val))
    if len(words) != len(desired):
        raise ValueError('wrong number of words')
    if tuple(bits_from_mwot(val)) != desired:
        raise ValueError(f'bits not {desired}')
    return words
