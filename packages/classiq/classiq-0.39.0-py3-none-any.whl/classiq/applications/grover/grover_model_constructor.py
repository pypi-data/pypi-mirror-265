from typing import Dict, List, Tuple

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
)
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.quantum_type import QuantumNumeric
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq import RegisterUserInput

_OUTPUT_VARIABLE_NAME = "result"

_PREDICATE_FUNCTION_NAME = "expr_predicate"


def _arithmetic_oracle_io_dict(
    definitions: List[Tuple[str, RegisterUserInput]], handle_name: str
) -> Dict[str, HandleBinding]:
    cursor = 0
    ios: Dict[str, HandleBinding] = dict()
    for reg_name, reg in definitions:
        ios[reg_name] = SlicedHandleBinding(
            name=handle_name,
            start=Expression(expr=f"{cursor}"),
            end=Expression(expr=f"{cursor + reg.size}"),
        )
        cursor += reg.size
    return ios


def _construct_arithmetic_oracle(
    predicate_function: str,
    definitions: List[Tuple[str, RegisterUserInput]],
) -> QuantumFunctionCall:
    predicate_var_binding = _arithmetic_oracle_io_dict(definitions, "arg0")
    predicate_var_binding["res"] = HandleBinding(name="arg1")
    return QuantumFunctionCall(
        function="phase_oracle",
        inouts={
            "target": HandleBinding(name="arg0"),
        },
        operands={
            "predicate": QuantumLambdaFunction(
                body=[
                    QuantumFunctionCall(
                        function=predicate_function,
                        inouts=predicate_var_binding,
                    ),
                ],
            ),
        },
    )


def grover_main_port_declarations(
    definitions: List[Tuple[str, RegisterUserInput]],
    direction: PortDeclarationDirection,
) -> Dict[str, PortDeclaration]:
    return {
        name: PortDeclaration(
            name=name,
            size=Expression(expr=f"{reg.size}"),
            quantum_type=QuantumNumeric(
                size=Expression(expr=f"{reg.size}"),
                is_signed=Expression(expr=f"{reg.is_signed}"),
                fraction_digits=Expression(expr=f"{reg.fraction_places}"),
            ),
            direction=direction,
        )
        for name, reg in definitions
    }


def construct_grover_model(
    definitions: List[Tuple[str, RegisterUserInput]],
    expression: str,
    num_reps: int = 1,
) -> SerializedModel:
    predicate_port_decls = grover_main_port_declarations(
        definitions, PortDeclarationDirection.Inout
    )
    predicate_port_decls["res"] = PortDeclaration(
        name="res",
        size=Expression(expr="1"),
        direction=PortDeclarationDirection.Inout,
    )
    num_qubits = sum(reg.size for _, reg in definitions)

    grover_model = Model(
        functions=[
            NativeFunctionDefinition(
                name=_PREDICATE_FUNCTION_NAME,
                port_declarations=predicate_port_decls,
                body=[
                    ArithmeticOperation(
                        expression=Expression(expr=expression),
                        result_var=HandleBinding(name="res"),
                        inplace_result=True,
                    ),
                ],
            ),
            NativeFunctionDefinition(
                name="main",
                port_declarations=grover_main_port_declarations(
                    definitions, PortDeclarationDirection.Output
                ),
                body=[
                    VariableDeclarationStatement(name="packed_vars"),
                    QuantumFunctionCall(
                        function="allocate",
                        positional_args=[
                            Expression(expr=f"{num_qubits}"),
                            HandleBinding(name="packed_vars"),
                        ],
                    ),
                    QuantumFunctionCall(
                        function="grover_search",
                        params={
                            "reps": Expression(expr=f"{num_reps}"),
                        },
                        inouts={"packed_vars": HandleBinding(name="packed_vars")},
                        operands={
                            "oracle": QuantumLambdaFunction(
                                body=[
                                    _construct_arithmetic_oracle(
                                        _PREDICATE_FUNCTION_NAME,
                                        definitions,
                                    )
                                ]
                            )
                        },
                    ),
                    BindOperation(
                        in_handles=[HandleBinding(name="packed_vars")],
                        out_handles=[
                            HandleBinding(name=name) for name, _ in definitions
                        ],
                    ),
                ],
            ),
        ],
    )
    return grover_model.get_model()
