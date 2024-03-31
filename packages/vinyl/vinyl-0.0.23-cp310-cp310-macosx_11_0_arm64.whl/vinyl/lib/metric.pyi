import ibis.expr.types as ir
from typing import Any, Callable, Sequence
from vinyl.lib.column import VinylColumn as VinylColumn
from vinyl.lib.column_methods import ColumnBuilder as ColumnBuilder, ColumnListBuilder as ColumnListBuilder, column_type as column_type
from vinyl.lib.enums import FillOptions as FillOptions, WindowType as WindowType
from vinyl.lib.table import VinylTable as VinylTable

class Metric:
    def __init__(self, tbl: VinylTable, agg: Callable[..., Any], ts: Callable[..., Any], by: column_type, fill=...) -> None: ...

class MetricStore:
    __dict__: dict[str, Any]
    def __init__(self, metrics: Sequence[Metric] = [], derived_metrics: dict[str, ir.Deferred] = {}, default_tbl: VinylTable | None = None) -> None: ...
    def __getattr__(self, name) -> VinylColumn: ...
    def __add__(self, other: MetricStore) -> MetricStore: ...
    def __radd__(self, other: MetricStore) -> MetricStore: ...
    def __call__(self): ...
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    def select(self, cols: column_type, trailing: list[int | None] = [None]) -> VinylTable:
        """
        Retrieves the selected columns from the MetricStore.

        For `cols`, you may select metrics, dimensions, or the timestamp column. You can also select any expressions (e.g. met1 + met2) based on metrics or dimensions, but not a mix of metrics and dimensions in the same expression. If you select the timestamp column, you must use the `.floor` method to bucket the timestamps to a desired interval.

        If no trailing intervals are provided, the function will return the aggregated value for each col. If you provide trailing intervals, the function will return the aggregated value over the trailing intervals. For example, if you provide [1, 2], the function will return the aggregated value **for each `col`** over the interval and the previous interval, and the aggregated value over the interval and the previous two intervals.
        """
    def metric(self, cols: ir.Scalar | Callable[..., ir.Scalar] | list[ir.Scalar | Callable[..., ir.Scalar]] | dict[str, ir.Scalar | Callable[..., ir.Scalar]], ts: ir.TimestampValue | Callable[..., ir.TimestampValue], by: ir.Value | Callable[..., ir.Value] | Sequence[ir.Value | Callable[..., ir.Value]] = [], fill: FillOptions | Callable[..., Any] = ..., tbl: VinylTable | None = None): ...
    def derive(self, metrics: ir.Scalar | Callable[..., ir.Scalar] | list[ir.Scalar | Callable[..., ir.Scalar]] | dict[str, ir.Scalar | Callable[..., ir.Scalar]]):
        """
        Add a derived metric to the MetricStore. Derived metrics are calculated from existing metrics in the MetricStore.

        Please do not include any other columns in the derived metric. This could cause unexpected behavior.
        """

class MetricSelect:
    def __init__(self, MetricStore: MetricStore, cols: list[ir.Value], intervals: list[int | None] = [None]) -> None: ...
