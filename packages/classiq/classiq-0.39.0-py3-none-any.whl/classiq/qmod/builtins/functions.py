# This file was generated automatically - do not edit manually

from typing import List, Literal

from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.qmod_variable import Input, Output, QArray, QBit, QNum
from classiq.qmod.quantum_callable import QCallable, QCallableList

from .structs import *


@qfunc(external=True)
def permute(
    functions: QCallableList,
) -> None:
    pass


@qfunc(external=True)
def apply(
    operand: QCallable,
) -> None:
    pass


@qfunc(external=True)
def molecule_ucc(
    molecule_problem: QParam[MoleculeProblem],
    excitations: QParam[List[int]],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def molecule_hva(
    molecule_problem: QParam[MoleculeProblem],
    reps: QParam[int],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def molecule_hartree_fock(
    molecule_problem: QParam[MoleculeProblem],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_ucc(
    fock_hamiltonian_problem: QParam[FockHamiltonianProblem],
    excitations: QParam[List[int]],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_hva(
    fock_hamiltonian_problem: QParam[FockHamiltonianProblem],
    reps: QParam[int],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def fock_hamiltonian_hartree_fock(
    fock_hamiltonian_problem: QParam[FockHamiltonianProblem],
    qbv: QArray[
        QBit,
        Literal[
            "len(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'))"
        ],
    ],
) -> None:
    pass


@qfunc(external=True)
def log_normal_finance(
    finance_model: QParam[LogNormalModel],
    finance_function: QParam[FinanceFunction],
    func_port: QArray[QBit, Literal["get_field(finance_model, 'num_qubits')"]],
    obj_port: QBit,
) -> None:
    pass


@qfunc(external=True)
def gaussian_finance(
    finance_model: QParam[GaussianModel],
    finance_function: QParam[FinanceFunction],
    func_port: QArray[
        QBit,
        Literal[
            "get_field(finance_model, 'num_qubits') + len(get_field(finance_model, 'rhos')) + floor(log(sum(get_field(finance_model, 'loss')), 2)) + 1"
        ],
    ],
    obj_port: QBit,
) -> None:
    pass


@qfunc(external=True)
def pauli_feature_map(
    feature_map: QParam[QSVMFeatureMapPauli],
    qbv: QArray[QBit, Literal["get_field(feature_map, 'feature_dimension')"]],
) -> None:
    pass


@qfunc(external=True)
def bloch_sphere_feature_map(
    feature_dimension: QParam[int],
    qbv: QArray[QBit, Literal["ceiling(feature_dimension/2)"]],
) -> None:
    pass


@qfunc(external=True)
def H(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def X(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def Y(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def Z(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def I(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def S(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def T(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def SDG(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def TDG(
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def PHASE(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def RX(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def RY(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def RZ(
    theta: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def R(
    theta: QParam[float],
    phi: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def RXX(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@qfunc(external=True)
def RYY(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@qfunc(external=True)
def RZZ(
    theta: QParam[float],
    target: QArray[QBit, Literal[2]],
) -> None:
    pass


@qfunc(external=True)
def CH(
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CX(
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CY(
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CZ(
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CRX(
    theta: QParam[float],
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CRY(
    theta: QParam[float],
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CRZ(
    theta: QParam[float],
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CPHASE(
    theta: QParam[float],
    control: QBit,
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def SWAP(
    qbit0: QBit,
    qbit1: QBit,
) -> None:
    pass


@qfunc(external=True)
def IDENTITY(
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def prepare_state(
    probabilities: QParam[List[float]],
    bound: QParam[float],
    out: Output[QArray[QBit, Literal["log(len(probabilities), 2)"]]],
) -> None:
    pass


@qfunc(external=True)
def prepare_amplitudes(
    amplitudes: QParam[List[float]],
    bound: QParam[float],
    out: Output[QArray[QBit, Literal["log(len(amplitudes), 2)"]]],
) -> None:
    pass


@qfunc(external=True)
def unitary(
    elements: QParam[List[List[float]]],
    target: QArray[QBit, Literal["log(len(elements[0]), 2)"]],
) -> None:
    pass


@qfunc(external=True)
def add(
    left: QArray[QBit],
    right: QArray[QBit],
    result: Output[QArray[QBit, Literal["Max(len(left), len(right)) + 1"]]],
) -> None:
    pass


@qfunc(external=True)
def modular_add(
    left: QArray[QBit],
    right: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def integer_xor(
    left: QArray[QBit],
    right: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def U(
    theta: QParam[float],
    phi: QParam[float],
    lam: QParam[float],
    gam: QParam[float],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def CCX(
    control: QArray[QBit, Literal[2]],
    target: QBit,
) -> None:
    pass


@qfunc(external=True)
def allocate(
    num_qubits: QParam[int],
    out: Output[QArray[QBit, Literal["num_qubits"]]],
) -> None:
    pass


@qfunc(external=True)
def free(
    in_: Input[QArray[QBit]],
) -> None:
    pass


@qfunc(external=True)
def randomized_benchmarking(
    num_of_cliffords: QParam[int],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def inplace_prepare_state(
    probabilities: QParam[List[float]],
    bound: QParam[float],
    target: QArray[QBit, Literal["log(len(probabilities), 2)"]],
) -> None:
    pass


@qfunc(external=True)
def inplace_prepare_amplitudes(
    amplitudes: QParam[List[float]],
    bound: QParam[float],
    target: QArray[QBit, Literal["log(len(amplitudes), 2)"]],
) -> None:
    pass


@qfunc(external=True)
def single_pauli_exponent(
    pauli_string: QParam[List[int]],
    coefficient: QParam[float],
    qbv: QArray[QBit, Literal["len(pauli_string)"]],
) -> None:
    pass


@qfunc(external=True)
def suzuki_trotter(
    pauli_operator: QParam[List[PauliTerm]],
    evolution_coefficient: QParam[float],
    order: QParam[int],
    repetitions: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@qfunc(external=True)
def qdrift(
    pauli_operator: QParam[List[PauliTerm]],
    evolution_coefficient: QParam[float],
    num_qdrift: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@qfunc(external=True)
def exponentiation_with_depth_constraint(
    pauli_operator: QParam[List[PauliTerm]],
    evolution_coefficient: QParam[float],
    max_depth: QParam[int],
    qbv: QArray[QBit, Literal["len(get_field(pauli_operator[0], 'pauli'))"]],
) -> None:
    pass


@qfunc(external=True)
def qft_step(
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qft(
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qpe_flexible(
    unitary_with_power: QCallable[QParam[int]],
    phase: QNum,
) -> None:
    pass


@qfunc(external=True)
def qpe(
    unitary: QCallable,
    phase: QNum,
) -> None:
    pass


@qfunc(external=True)
def single_pauli(
    slope: QParam[float],
    offset: QParam[float],
    q1_qfunc: QCallable[QParam[float], QBit],
    x: QArray[QBit],
    q: QBit,
) -> None:
    pass


@qfunc(external=True)
def linear_pauli_rotations(
    bases: QParam[List[int]],
    slopes: QParam[List[float]],
    offsets: QParam[List[float]],
    x: QArray[QBit],
    q: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def amplitude_estimation(
    oracle: QCallable[QArray[QBit]],
    space_transform: QCallable[QArray[QBit]],
    phase: QNum,
    packed_vars: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def phase_oracle(
    predicate: QCallable[QArray[QBit], QArray[QBit]],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def reflect_about_zero(
    packed_vars: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def grover_diffuser(
    space_transform: QCallable[QArray[QBit]],
    packed_vars: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def grover_operator(
    oracle: QCallable[QArray[QBit]],
    space_transform: QCallable[QArray[QBit]],
    packed_vars: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def grover_search(
    reps: QParam[int],
    oracle: QCallable[QArray[QBit]],
    packed_vars: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def hadamard_transform(
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def apply_to_all(
    gate_operand: QCallable[QBit],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def allocate_num(
    num_qubits: QParam[int],
    is_signed: QParam[bool],
    fraction_digits: QParam[int],
    out: Output[QNum],
) -> None:
    pass


@qfunc(external=True)
def qaoa_mixer_layer(
    b: QParam[float],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qaoa_cost_layer(
    g: QParam[float],
    hamiltonian: QParam[List[PauliTerm]],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qaoa_layer(
    g: QParam[float],
    b: QParam[float],
    hamiltonian: QParam[List[PauliTerm]],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qaoa_init(
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def qaoa_penalty(
    num_qubits: QParam[int],
    params_list: QParam[List[float]],
    hamiltonian: QParam[List[PauliTerm]],
    target: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@qfunc(external=True)
def full_hea(
    num_qubits: QParam[int],
    is_parametrized: QParam[List[int]],
    angle_params: QParam[List[float]],
    connectivity_map: QParam[List[List[int]]],
    reps: QParam[int],
    operands_1qubit: QCallableList[QParam[float], QBit],
    operands_2qubit: QCallableList[QParam[float], QBit, QBit],
    x: QArray[QBit, Literal["num_qubits"]],
) -> None:
    pass


@qfunc(external=True)
def swap_test(
    state1: QArray[QBit],
    state2: QArray[QBit],
    test: Output[QArray[QBit]],
) -> None:
    pass


@qfunc(external=True)
def prepare_ghz_state(
    size: QParam[int],
    q: Output[QArray[QBit]],
) -> None:
    pass


@qfunc(external=True)
def prepare_exponential_state(
    rate: QParam[int],
    q: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def prepare_bell_state(
    state_num: QParam[int],
    q: Output[QArray[QBit]],
) -> None:
    pass


@qfunc(external=True)
def inplace_prepare_int(
    value: QParam[int],
    target: QArray[QBit],
) -> None:
    pass


@qfunc(external=True)
def prepare_int(
    value: QParam[int],
    out: Output[QNum],
) -> None:
    pass


@qfunc(external=True)
def switch(
    selector: QParam[int],
    cases: QCallableList,
) -> None:
    pass


__all__ = [
    "permute",
    "apply",
    "molecule_ucc",
    "molecule_hva",
    "molecule_hartree_fock",
    "fock_hamiltonian_ucc",
    "fock_hamiltonian_hva",
    "fock_hamiltonian_hartree_fock",
    "log_normal_finance",
    "gaussian_finance",
    "pauli_feature_map",
    "bloch_sphere_feature_map",
    "H",
    "X",
    "Y",
    "Z",
    "I",
    "S",
    "T",
    "SDG",
    "TDG",
    "PHASE",
    "RX",
    "RY",
    "RZ",
    "R",
    "RXX",
    "RYY",
    "RZZ",
    "CH",
    "CX",
    "CY",
    "CZ",
    "CRX",
    "CRY",
    "CRZ",
    "CPHASE",
    "SWAP",
    "IDENTITY",
    "prepare_state",
    "prepare_amplitudes",
    "unitary",
    "add",
    "modular_add",
    "integer_xor",
    "U",
    "CCX",
    "allocate",
    "free",
    "randomized_benchmarking",
    "inplace_prepare_state",
    "inplace_prepare_amplitudes",
    "single_pauli_exponent",
    "suzuki_trotter",
    "qdrift",
    "exponentiation_with_depth_constraint",
    "qft_step",
    "qft",
    "qpe_flexible",
    "qpe",
    "single_pauli",
    "linear_pauli_rotations",
    "amplitude_estimation",
    "phase_oracle",
    "reflect_about_zero",
    "grover_diffuser",
    "grover_operator",
    "grover_search",
    "hadamard_transform",
    "apply_to_all",
    "allocate_num",
    "qaoa_mixer_layer",
    "qaoa_cost_layer",
    "qaoa_layer",
    "qaoa_init",
    "qaoa_penalty",
    "full_hea",
    "swap_test",
    "prepare_ghz_state",
    "prepare_exponential_state",
    "prepare_bell_state",
    "inplace_prepare_int",
    "prepare_int",
    "switch",
]
