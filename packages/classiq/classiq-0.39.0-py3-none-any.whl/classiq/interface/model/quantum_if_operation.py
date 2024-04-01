from typing import TYPE_CHECKING, Optional

import pydantic
from sympy import Equality
from sympy.core.numbers import Integer

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qscalar_proxy import QmodQNumProxy
from classiq.interface.model.quantum_expressions.control_state import (
    min_bit_length,
    to_twos_complement,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)

from classiq.exceptions import ClassiqValueError

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock

QUANTUM_IF_INOUT_NAME = "ctrl"
QUANTUM_IF_CONDITION_ARG_ERROR_MESSAGE_FORMAT = (
    "quantum_if condition must be of the form '<quantum-variable> == "
    "<classical-integer-expression>', but condition's {}-hand side was {!r}"
)


class QuantumIf(QuantumExpressionOperation):
    then: "StatementBlock"
    _ctrl: Optional[QmodQNumProxy] = pydantic.PrivateAttr(
        default=None,
    )
    _ctrl_val: Optional[int] = pydantic.PrivateAttr(
        default=None,
    )

    @property
    def condition(self) -> Expression:
        return self.expression

    @property
    def ctrl(self) -> QmodQNumProxy:
        assert self._ctrl is not None
        return self._ctrl

    @property
    def ctrl_val(self) -> int:
        assert self._ctrl_val is not None
        return self._ctrl_val

    def resolve_condition(self) -> None:
        condition = self.condition.value.value
        if not isinstance(condition, Equality):
            raise ClassiqValueError(
                f"quantum_if condition must be an equality, was {str(condition)!r}"
            )
        ctrl, ctrl_val = condition.args
        if isinstance(ctrl, Integer) and isinstance(ctrl_val, QmodQNumProxy):
            ctrl, ctrl_val = ctrl_val, ctrl
        if not isinstance(ctrl, QmodQNumProxy):
            raise ClassiqValueError(
                QUANTUM_IF_CONDITION_ARG_ERROR_MESSAGE_FORMAT.format("left", str(ctrl))
            )
        if not isinstance(ctrl_val, Integer):
            raise ClassiqValueError(
                QUANTUM_IF_CONDITION_ARG_ERROR_MESSAGE_FORMAT.format(
                    "right", str(ctrl_val)
                )
            )
        self._ctrl, self._ctrl_val = ctrl, int(ctrl_val)

    @property
    def ctrl_state(self) -> str:
        is_signed = self.ctrl.is_signed
        fraction_places = self.ctrl.fraction_digits
        ctrl_size = len(self.ctrl)
        if not is_signed and self.ctrl_val < 0:
            raise ClassiqValueError(
                f"Variable {str(self.ctrl)!r} is not signed but control value "
                f"{self.ctrl_val} is negative"
            )
        required_qubits = min_bit_length(self.ctrl_val, is_signed)
        if ctrl_size < required_qubits:
            raise ClassiqValueError(
                f"Variable {str(self.ctrl)!r} has {ctrl_size} qubits but control value "
                f"{str(self.ctrl_val)!r} requires at least {required_qubits} qubits"
            )
        if fraction_places != 0:
            raise ClassiqValueError(
                f"quantum-if on a non-integer quantum variable {str(self.ctrl)!r} is "
                f"not supported at the moment"
            )
        return to_twos_complement(self.ctrl_val, ctrl_size, is_signed)
