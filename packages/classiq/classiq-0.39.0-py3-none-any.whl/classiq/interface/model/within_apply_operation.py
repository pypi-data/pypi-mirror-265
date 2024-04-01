from typing import TYPE_CHECKING

from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class WithinApply(QuantumOperation):
    compute: "StatementBlock"
    action: "StatementBlock"
