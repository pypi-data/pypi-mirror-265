from typing import Optional

from pyomo import environ as pyo
from pyomo.core import Objective, maximize

from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalList,
    Real,
    Struct,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall

from classiq.applications.combinatorial_helpers.combinatorial_problem_utils import (
    _internal_pyo_model_to_hamiltonian,
    compute_qaoa_initial_point,
    convert_pyomo_to_global_presentation,
)
from classiq.applications.combinatorial_helpers.pauli_helpers.pauli_utils import (
    _pauli_operator_to_qmod,
    get_pauli_operator,
)
from classiq.applications.combinatorial_optimization import OptimizerConfig, QAOAConfig


def construct_combi_opt_py_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> Model:
    if qaoa_config is None:
        qaoa_config = QAOAConfig()

    if optimizer_config is None:
        optimizer_config = OptimizerConfig()

    max_iteration = 0
    if optimizer_config.max_iteration is not None:
        max_iteration = optimizer_config.max_iteration

    hamiltonian = _internal_pyo_model_to_hamiltonian(
        pyo_model, qaoa_config.penalty_energy
    )
    qaoa_initial_point = compute_qaoa_initial_point(hamiltonian, qaoa_config.num_layers)
    len_hamiltonian = len(hamiltonian[0]["pauli"])
    pauli_oper = get_pauli_operator(hamiltonian)
    pauli_qmod = _pauli_operator_to_qmod(pauli_oper)

    initial_point_expression = (
        f"{optimizer_config.initial_point}"
        if optimizer_config.initial_point is not None
        else f"{qaoa_initial_point}"
    )

    return Model(
        constants=[
            Constant(
                name="hamiltonian",
                const_type=ClassicalList(element_type=Struct(name="PauliTerm")),
                value=Expression(expr=f"[{pauli_qmod}]"),
            )
        ],
        functions=[
            NativeFunctionDefinition(
                name="main",
                param_decls={
                    "params_list": ClassicalArray(
                        element_type=Real(), size=qaoa_config.num_layers * 2
                    )
                },
                port_declarations={
                    "target": PortDeclaration(
                        name="target",
                        size=Expression(expr=f"{len_hamiltonian}"),
                        direction=PortDeclarationDirection.Output,
                    ),
                },
                body=[
                    QuantumFunctionCall(
                        function="allocate",
                        positional_args=[
                            Expression(expr="len(target)"),
                            HandleBinding(name="target"),
                        ],
                    ),
                    QuantumFunctionCall(
                        function="qaoa_penalty",
                        params={
                            "num_qubits": Expression(expr="len(target)"),
                            "params_list": Expression(expr="params_list"),
                            "hamiltonian": Expression(expr="hamiltonian"),
                        },
                        inouts={"target": HandleBinding(name="target")},
                    ),
                ],
            ),
        ],
        classical_execution_code=f"""
vqe_result = vqe(
hamiltonian=hamiltonian,
maximize={next(pyo_model.component_objects(Objective)).sense == maximize},
initial_point={initial_point_expression},
optimizer=Optimizer.{optimizer_config.opt_type},
max_iteration={max_iteration},
tolerance={optimizer_config.tolerance},
step_size={optimizer_config.step_size},
skip_compute_variance={optimizer_config.skip_compute_variance},
alpha_cvar={optimizer_config.alpha_cvar}
)

save({{"vqe_result": vqe_result, "hamiltonian": hamiltonian}})
""",
    )


def construct_combinatorial_optimization_model(
    pyo_model: pyo.ConcreteModel,
    qaoa_config: Optional[QAOAConfig] = None,
    optimizer_config: Optional[OptimizerConfig] = None,
) -> SerializedModel:
    converted_pyo_model = convert_pyomo_to_global_presentation(pyo_model)
    model = construct_combi_opt_py_model(
        converted_pyo_model, qaoa_config, optimizer_config
    )
    return model.get_model()
