from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.functions.classical_type import ConcreteClassicalType


class ClassicalParameterDeclaration(ASTNode):
    name: str
    classical_type: ConcreteClassicalType
