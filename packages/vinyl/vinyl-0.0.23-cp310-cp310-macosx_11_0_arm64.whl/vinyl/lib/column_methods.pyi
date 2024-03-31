import ibis.expr.types as ir
from ibis import selectors as s
from ibis.common.deferred import Deferred
from typing import TypeAlias
from vinyl.lib.graph import VinylGraph as VinylGraph

base_column_type: TypeAlias
base_boolean_column_type: TypeAlias
boolean_column_type: TypeAlias
column_type_without_dict: TypeAlias
column_type: TypeAlias
column_type_all: TypeAlias

class ColumnBuilder:
    def __init__(self, tbl: ir.Table, col: base_column_type | s.Selector | None, passthrough_deferred: bool = False) -> None: ...

class ColumnListBuilder:
    def __init__(self, tbl: ir.Table, cols: dict[str, Deferred | ir.Value] | list[Deferred | ir.Value | s.Selector] | Deferred | ir.Value | s.Selector | None, unique: bool = False, passthrough_deferred: bool = False) -> None: ...
    def __iter__(self): ...
    def __add__(self, other) -> ColumnListBuilder: ...
    def __radd__(self, other) -> ColumnListBuilder: ...

class SortColumnListBuilder(ColumnListBuilder):
    def __init__(self, tbl, cols, reverse: bool = False, unique: bool = False, passthrough_deferred: bool = False) -> None: ...

class ColumnHelper(ir.ArrayColumn, ir.BinaryColumn, ir.BooleanColumn, ir.DecimalColumn, ir.FloatingColumn, ir.INETColumn, ir.IntervalColumn, ir.JSONColumn, ir.LineStringColumn, ir.MACADDRColumn, ir.MapColumn, ir.MultiLineStringColumn, ir.MultiPointColumn, ir.MultiPolygonColumn, ir.NullColumn, ir.PointColumn, ir.PolygonColumn, ir.StringColumn, ir.TimestampColumn, ir.IntegerColumn, ir.UUIDColumn):
    def __init__(self, *args, **kwargs) -> None: ...
