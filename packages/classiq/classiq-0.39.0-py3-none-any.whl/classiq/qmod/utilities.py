import keyword
import sys
from typing import get_args, get_origin

DEFAULT_DECIMAL_PRECISION = 4


def mangle_keyword(name: str) -> str:
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def unmangle_keyword(name: str) -> str:
    assert name
    if name[-1] == "_" and keyword.iskeyword(name[:-1]):
        name = name[:-1]
    return name


def version_portable_get_args(py_type: type) -> tuple:
    if get_origin(py_type) is None:
        return tuple()
    if sys.version_info[0:2] < (3, 10):
        return get_args(py_type)  # The result of __class_getitem__
    else:
        return get_args(py_type)[0]
