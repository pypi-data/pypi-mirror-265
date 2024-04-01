from typing import TYPE_CHECKING

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class Power(QuantumOperation):
    power: Expression
    body: "StatementBlock"
