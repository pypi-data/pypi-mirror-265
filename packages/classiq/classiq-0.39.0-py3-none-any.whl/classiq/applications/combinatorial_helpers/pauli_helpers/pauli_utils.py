from typing import List, cast

from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.generator.expressions.enums.pauli import Pauli
from classiq.interface.generator.functions.qmod_python_interface import QmodPyStruct
from classiq.interface.helpers.custom_pydantic_types import PydanticPauliList

from classiq.exceptions import (
    ClassiqExecutorInvalidHamiltonianError,
    ClassiqNonNumericCoefficientInPauliError,
    ClassiqValueError,
)


class PauliTerm:
    pauli: List[int]
    coefficient: float


def pauli_string_to_int(pauli_str: str) -> List[int]:
    pauli_map = {"I": 0, "X": 1, "Y": 2, "Z": 3}
    return [pauli_map[char] for char in pauli_str]


def _pauli_str_to_enums(pauli_str: str) -> str:
    return ", ".join(f"Pauli.{pauli_term}" for pauli_term in pauli_str)


def pauli_integers_to_str(paulis: List[Pauli]) -> str:
    return "".join([Pauli(pauli).name for pauli in paulis])


def pauli_operator_to_hamiltonian(pauli_list: PydanticPauliList) -> List[QmodPyStruct]:
    pauli_struct_list: List[QmodPyStruct] = []
    for pauli_term in pauli_list:
        if not isinstance(pauli_term[1], complex) or pauli_term[1].imag != 0:
            raise ClassiqNonNumericCoefficientInPauliError(
                "Coefficient is not a number."
            )

        pauli_struct_list.append(
            {
                "pauli": [Pauli[p] for p in pauli_term[0]],
                "coefficient": pauli_term[1].real,
            }
        )
    return pauli_struct_list


def get_pauli_operator(pauli_operator: List[QmodPyStruct]) -> PauliOperator:
    pauli_list = [
        (
            pauli_integers_to_str(elem["pauli"]),
            elem["coefficient"],
        )
        for elem in pauli_operator
    ]

    try:
        pauli = PauliOperator(pauli_list=pauli_list)
    except ValueError:
        raise ClassiqExecutorInvalidHamiltonianError() from None

    return pauli


def _pauli_operator_to_qmod(hamiltonian: PauliOperator) -> str:
    if not all(isinstance(summand[1], complex) for summand in hamiltonian.pauli_list):
        raise ClassiqValueError(
            "Supporting only Hamiltonian with numeric coefficients."
        )
    return ", ".join(
        f"struct_literal(PauliTerm, pauli=[{_pauli_str_to_enums(pauli)}], coefficient={cast(complex, coeff).real})"
        for pauli, coeff in hamiltonian.pauli_list
    )
