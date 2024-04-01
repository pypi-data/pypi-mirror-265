from typing import TYPE_CHECKING, Dict, List, Optional, Union

import pydantic

from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.quantum_function_declaration import (
    QuantumOperandDeclaration,
)

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class QuantumLambdaFunction(ASTNode):
    """
    The definition of an anonymous function passed as operand to higher-level functions
    """

    rename_params: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="Mapping of the declared param to the actual variable name used ",
    )

    body: "StatementBlock" = pydantic.Field(
        description="A list of function calls passed to the operator"
    )

    _func_decl: Optional[QuantumOperandDeclaration] = pydantic.PrivateAttr(default=None)

    @property
    def func_decl(self) -> Optional[QuantumOperandDeclaration]:
        return self._func_decl

    def set_op_decl(self, fd: QuantumOperandDeclaration) -> None:
        self._func_decl = fd


class LambdaListComprehension(ASTNode):
    """
    Specification of a list of lambda functions iteratively
    """

    count: Expression = pydantic.Field(
        description="The number of lambda functions in the list"
    )

    index_var: str = pydantic.Field(
        description="The name of the integer variable holding the iteration index"
    )

    func: QuantumLambdaFunction = pydantic.Field(
        description="A lambda function definition replicated for index values 0 to count-1"
    )


QuantumCallable = Union[str, QuantumLambdaFunction]
QuantumOperand = Union[QuantumCallable, List[QuantumCallable], LambdaListComprehension]
