from typing import Tuple, Union

from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.symbolic_expr import SymbolicExpr

SymbolicTypes = Union[
    QParam, SymbolicExpr, int, float, bool, Tuple["SymbolicTypes", ...]
]
