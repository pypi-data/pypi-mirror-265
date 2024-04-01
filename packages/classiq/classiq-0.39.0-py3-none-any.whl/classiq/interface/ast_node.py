from typing import Optional

import pydantic

from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class SourceReference(pydantic.BaseModel):
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    file_name: Optional[str] = pydantic.Field(default=None)


class ASTNode(pydantic.BaseModel):
    source_ref: Optional[SourceReference] = pydantic.Field(default=None)


class HashableASTNode(ASTNode, HashablePydanticBaseModel):
    pass
