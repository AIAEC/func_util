from typing import Sequence


def is_namedtuple(value) -> bool:
    """
    predicate whether the type is a namedtuple
    :param value:
    :return:
    """
    _type = type(value)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False

    if not isinstance(getattr(_type, "_fields", None), tuple):
        return False

    return all(isinstance(sub, str) for sub in getattr(_type, "_fields", []))


def is_sequence(value, exclude_str_and_bytes: bool = True) -> bool:
    """
    predicate whether the type is a sequence
    :param value:
    :param exclude_str_and_bytes:
    :return:
    """
    if exclude_str_and_bytes and isinstance(value, (str, bytes)):
        return False

    return isinstance(value, Sequence)
