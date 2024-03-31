import ibis.expr.operations as ops
from ibis.expr.datatypes import DataType as DataType
from types import ModuleType
from typing import Any
from vinyl.lib.utils.obj import table_to_python_class as table_to_python_class

def get_caller_module(back: int) -> ModuleType | None: ...

class Field:
    name: str | None
    type: DataType | None
    description: str | None
    unique: bool
    primary_key: bool
    foreign_key: Field | tuple[str, str] | None
    pii: bool
    def __init__(self, name: str | None = None, type: DataType | None = None, description: str | None = None, primary_key: bool = False, foreign_key: Field | None = None, unique: bool = False, pii: bool = False, parent_name: str | None = None, parent_ibis_table: ops.UnboundTable | None = None, parent_vinyl_table: Any | None = None) -> None: ...
    def process_foreign_key(self, foreign_key): ...
