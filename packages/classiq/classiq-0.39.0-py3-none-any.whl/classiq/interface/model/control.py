from typing import TYPE_CHECKING, Union

from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class Control(QuantumOperation):
    control: Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    body: "StatementBlock"
