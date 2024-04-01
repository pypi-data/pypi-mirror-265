from classiq.interface.generator.functions.builtins.quantum_operators import (
    get_single_empty_operand_operator,
)
from classiq.interface.generator.functions.classical_type import Bool, Integer
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)

_CTRL_FIELD_NAME = "ctrl"
CONTROL_OPERATOR = get_single_empty_operand_operator(
    operator_name="control",
    port_declarations={
        _CTRL_FIELD_NAME: PortDeclaration(
            name=_CTRL_FIELD_NAME,
            direction=PortDeclarationDirection.Inout,
        )
    },
)

REPEAT_OPERATOR = QuantumFunctionDeclaration(
    name="repeat",
    param_decls={"count": Integer()},
    operand_declarations={
        "iteration": QuantumOperandDeclaration(
            name="iteration", param_decls={"index": Integer()}
        )
    },
)
POWER_OPERATOR = get_single_empty_operand_operator(
    operator_name="power", param_decls={"power": Integer()}
)
INVERT_OPERATOR = get_single_empty_operand_operator(operator_name="invert")

IF_OPERATOR = QuantumFunctionDeclaration(
    name="if",
    param_decls={"condition": Bool()},
    operand_declarations={
        "then": QuantumOperandDeclaration(name="then"),
        "else": QuantumOperandDeclaration(name="else"),
    },
)
COMPUTE = get_single_empty_operand_operator(operator_name="compute")
UNCOMPUTE = get_single_empty_operand_operator(operator_name="uncompute")


INTERNAL_OPERATORS = nameables_to_dict(
    [
        CONTROL_OPERATOR,
        REPEAT_OPERATOR,
        POWER_OPERATOR,
        INVERT_OPERATOR,
        IF_OPERATOR,
        COMPUTE,
        UNCOMPUTE,
    ]
)
