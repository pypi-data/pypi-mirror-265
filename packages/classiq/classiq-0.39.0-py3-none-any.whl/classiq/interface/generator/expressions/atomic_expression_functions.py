SUPPORTED_BUILTIN_FUNCTIONS = {"len", "sum", "print"}

SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS = {
    "hypercube_entangler_graph",
    "grid_entangler_graph",
    "qft_const_adder_phase",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
    "get_type",
    "struct_literal",
    "get_field",
    "fraction_digits",
    "is_signed",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "molecule_ground_state_solution_post_process",
    "BitwiseAnd",
    "BitwiseXor",
    "BitwiseNot",
    "BitwiseOr",
    *SUPPORTED_BUILTIN_FUNCTIONS,
}
