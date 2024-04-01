# This file was generated automatically - do not edit manually

from typing import List

from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.symbolic import symbolic_function

from .structs import *


def qft_const_adder_phase(
    bit_index: QParam[int],
    value: QParam[int],
    reg_len: QParam[int],
) -> QParam[float]:
    return symbolic_function(bit_index, value, reg_len, return_type=QParam[float])


def molecule_problem_to_hamiltonian(
    problem: QParam[MoleculeProblem],
) -> QParam[List[PauliTerm]]:
    return symbolic_function(problem, return_type=QParam[List[PauliTerm]])


def fock_hamiltonian_problem_to_hamiltonian(
    problem: QParam[FockHamiltonianProblem],
) -> QParam[List[PauliTerm]]:
    return symbolic_function(problem, return_type=QParam[List[PauliTerm]])


def grid_entangler_graph(
    num_qubits: QParam[int],
    schmidt_rank: QParam[int],
    grid_randomization: QParam[bool],
) -> QParam[List[List[int]]]:
    return symbolic_function(
        num_qubits,
        schmidt_rank,
        grid_randomization,
        return_type=QParam[List[List[int]]],
    )


def hypercube_entangler_graph(
    num_qubits: QParam[int],
) -> QParam[List[List[int]]]:
    return symbolic_function(num_qubits, return_type=QParam[List[List[int]]])


def log_normal_finance_post_process(
    finance_model: QParam[LogNormalModel],
    estimation_method: QParam[FinanceFunction],
    probability: QParam[float],
) -> QParam[float]:
    return symbolic_function(
        finance_model, estimation_method, probability, return_type=QParam[float]
    )


def gaussian_finance_post_process(
    finance_model: QParam[GaussianModel],
    estimation_method: QParam[FinanceFunction],
    probability: QParam[float],
) -> QParam[float]:
    return symbolic_function(
        finance_model, estimation_method, probability, return_type=QParam[float]
    )


__all__ = [
    "qft_const_adder_phase",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "grid_entangler_graph",
    "hypercube_entangler_graph",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
]
