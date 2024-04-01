import sys
from typing import (  # type: ignore[attr-defined]
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    Union,
    _GenericAlias,
)

from typing_extensions import ParamSpec

from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalList,
    ClassicalType,
    Struct,
)

from classiq import StructDeclaration
from classiq.exceptions import ClassiqValueError
from classiq.qmod.model_state_container import ModelStateContainer
from classiq.qmod.symbolic_expr import Symbolic, SymbolicExpr

_T = TypeVar("_T")


if TYPE_CHECKING:

    class QParam(SymbolicExpr, Generic[_T]):
        pass

else:

    class QParam(Symbolic, Generic[_T]):
        pass


class QParamScalar(QParam, SymbolicExpr):
    pass


class QParamList(QParam):
    def __init__(
        self,
        expr: str,
        list_type: Union[ClassicalList, ClassicalArray],
        qmodule: ModelStateContainer,
    ) -> None:
        super().__init__(expr)
        self._qmodule = qmodule
        self._list_type = list_type

    def __getitem__(self, key: Any) -> QParam:
        return create_param(
            f"({self})[{key}]",
            self._list_type.element_type,
            qmodule=self._qmodule,
        )

    def __len__(self) -> int:
        raise ClassiqValueError(
            "len(<expr>) is not supported for QMod lists - use <expr>.len instead"
        )

    @property
    def len(self) -> QParamScalar:
        return QParamScalar(f"len({self})")


class QParamStruct(QParam):
    def __init__(
        self, expr: str, struct_type: Struct, *, qmodule: ModelStateContainer
    ) -> None:
        super().__init__(expr)
        self._qmodule = qmodule
        self._struct_type = struct_type

    def __getattr__(self, field_name: str) -> QParam:
        return QParamStruct.get_field(
            self._qmodule, str(self), self._struct_type.name, field_name
        )

    @staticmethod
    def get_field(
        qmodule: ModelStateContainer,
        variable_name: str,
        struct_name: str,
        field_name: str,
    ) -> QParam:
        struct_decl = StructDeclaration.BUILTIN_STRUCT_DECLARATIONS.get(
            struct_name, qmodule.type_decls.get(struct_name)
        )
        assert struct_decl is not None
        field_type = struct_decl.variables.get(field_name)
        if field_type is None:
            raise ClassiqValueError(
                f"Struct {struct_name!r} doesn't have field {field_name!r}"
            )

        return create_param(
            f"get_field({variable_name},{field_name!r})",
            field_type,
            qmodule=qmodule,
        )


_P = ParamSpec("_P")


class ArrayBase(Generic[_P]):
    # Support comma-separated generic args in older Python versions
    if sys.version_info[0:2] < (3, 10):

        def __class_getitem__(cls, args) -> _GenericAlias:
            return _GenericAlias(cls, args)


class Array(ArrayBase[_P]):
    pass


def create_param(
    expr_str: str, ctype: ClassicalType, qmodule: ModelStateContainer
) -> QParam:
    if isinstance(ctype, (ClassicalList, ClassicalArray)):
        return QParamList(expr_str, ctype, qmodule=qmodule)
    elif isinstance(ctype, Struct):
        return QParamStruct(expr_str, ctype, qmodule=qmodule)
    else:
        return QParamScalar(expr_str)
