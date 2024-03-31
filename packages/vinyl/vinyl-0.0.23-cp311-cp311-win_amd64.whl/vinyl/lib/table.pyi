import ibis.expr.operations as ops
import ibis.expr.types as ir
import ibis.selectors as s
import pandas as pd
import polars as pl
import pyarrow as pa
from ibis import Schema as Schema
from pathlib import Path
from typing import Any, Callable, Literal, Sequence
from vinyl.lib.chart import geom as geom
from vinyl.lib.column import VinylColumn as VinylColumn
from vinyl.lib.column_methods import ColumnBuilder as ColumnBuilder, ColumnListBuilder as ColumnListBuilder, SortColumnListBuilder as SortColumnListBuilder, base_boolean_column_type as base_boolean_column_type, base_column_type as base_column_type, boolean_column_type as boolean_column_type, column_type as column_type, column_type_all as column_type_all, column_type_without_dict as column_type_without_dict
from vinyl.lib.enums import FillOptions as FillOptions, WindowType as WindowType
from vinyl.lib.field import Field as Field
from vinyl.lib.graph import VinylGraph as VinylGraph
from vinyl.lib.metric import MetricStore as MetricStore
from vinyl.lib.schema import VinylSchema as VinylSchema
from vinyl.lib.table_methods import fill_type as fill_type
from vinyl.lib.utils.obj import is_valid_class_name as is_valid_class_name, to_valid_class_name as to_valid_class_name

class VinylTable:
    def __init__(self, _arg: ir.Expr, _conn_replace: dict[ops.Relation, ops.Relation] = {}, _twin_conn_replace: dict[ops.Relation, ops.Relation] = {}, _col_replace: dict[ops.Relation, dict[str, str]] = {}) -> None: ...
    def __call__(self) -> VinylTable: ...
    def __getattr__(self, name) -> VinylColumn: ...
    def __getitem__(self, key): ...
    def __enter__(self): ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    @property
    def tbl(self): ...
    def __add__(self, other) -> VinylTable: ...
    def __radd__(self, other) -> VinylTable: ...
    def __sub__(self, other) -> VinylTable: ...
    def __rsub__(self, other) -> VinylTable: ...
    def __mul__(self, other) -> VinylTable: ...
    def __rmul__(self, other) -> VinylTable: ...
    def select(self, cols: column_type, by: column_type | None = None, sort: column_type | None = None, window_type: WindowType = ..., window_bounds: tuple[int | None, int | None] = (None, None), fill: fill_type = None) -> VinylTable:
        """
        Computes a new table with the columns in cols. Can be a single column, a list of columns, or a dictionary of columns with their new names as keys. The column values themselves can be specified as strings (the column name), table attributes, one-argument lambda functions, or selectors.

        If an aggregated column is passed, this will be treated as a windowed column, using the by field for partitioning, the sort field for ordering, and the window_type and window_bounds fields for the actual window.

        Fill can be used optionally to add interpolation to cols. You must either specify one value for each column or a list of values that is the same length as the column list
        """
    def select_all(self, col_selector: column_type_all, f: Callable[[Any], Any] | list[Callable[[Any], Any] | None] | None, by: column_type | None = None, sort: column_type | None = None, window_type: WindowType = ..., window_bounds: tuple[int | None, int | None] = (None, None), fill: fill_type = None, rename: bool = False) -> VinylTable:
        """
        Select_all is a generalized form of `select` that can apply apply the same operation (specified in _f_) to multiple columns. The col_selector field can be a list of column fields, where each element  `select`, and _f_ should be a list of functions of the same length.

        If _f_ is a single function, it will be applied to all columns. If _f_ is a list of functions, the functions will be applied to the corresponding columns. If _f_ is shorter than the number of columns, the last function will be applied to all remaining columns.

        By, sort, window_type, and window_bounds operate as in `select`.

        If rename is True, the columns will be renamed to the name of the function that was applied to them. If rename is False, the columns will names to the original column name.
        """
    def define(self, cols: column_type, by: column_type | None = None, sort: column_type | None = None, window_type: WindowType = ..., window_bounds: tuple[int | None, int | None] = (None, None), fill: fill_type = None) -> VinylTable:
        """
        Mutate is identical to `select`, except all current columns are included, and the new columns are added to the table. If a new column has the same name as an existing column, the existing column will be replaced.
        """
    def define_all(self, col_selector: column_type_all, f: Callable[..., Any] | list[Callable[..., Any] | None] | None, by: column_type | None = None, sort: column_type | None = None, window_type: WindowType = ..., window_bounds: tuple[int | None, int | None] = (None, None), fill: fill_type = None, rename: bool = False) -> VinylTable:
        """
        Mutate_all is identical to `select_all`, except all current columns are included, and the new columns are added to the table. If a new column has the same name as an existing column, the existing column will be replaced.
        """
    def aggregate(self, cols: column_type, by: column_type | None = None, sort: column_type | None = None, fill: fill_type = None) -> VinylTable:
        """
        Returns an aggregated table for cols, grouped by `by` and `sort`.

        If fill is specified, the table will be interpolated using the specified fill strategy, taking into account direction from the `sort` argument. `fill` can either be a single value or a list of values, one for each column in `cols`.
        """
    def visualize(self):
        """
        Print a visualize representation of the query plan
        """
    def execute(self, format: Literal['pandas', 'polars', 'pyarrow', 'torch', 'text'] = 'pandas', twin: bool = False, limit: int | None = 10000) -> Any:
        """
        Run the query and return the result in the specified format. If twin is True, the twin connection will be used.
        """
    def save(self, path: str | Path, format: Literal['csv', 'delta', 'json', 'parquet'] = 'csv', twin: bool = False, limit: int = 10000):
        """
        Run the query and save the result to the specified path in the specified format.
        """
    def aggregate_all(self, col_selector: column_type_all, f: Callable[[Any], Any] | list[Callable[[Any], Any] | None] | None, by: column_type | None = None, sort: column_type | None = None, fill: fill_type = None, rename: bool = False) -> VinylTable:
        """
        Aggregate_all is a generalized form of `aggregate` that can apply apply the same operation (specified in _f_) to multiple columns. The col_selector field can be a list of column fields, where each element  `select`, and _f_ should be a list of functions of the same length.

        If _f_ is a single function, it will be applied to all columns. If _f_ is a list of functions, the functions will be applied to the corresponding columns. If _f_ is shorter than the number of columns, the last function will be applied to all remaining columns.

        By, sort, and fill operate as in `aggregate`.

        If rename is True, the columns will be renamed to the name of the function that was applied to them. If rename is False, the columns will names to the original column name.
        """
    def rename(self, rename_dict: dict[str, str]) -> VinylTable:
        """
        Rename columns in the table. The rename_dict should be a dictionary with the new column name as the key and the original column name as the value.
        """
    def relocate(self, cols: column_type_without_dict, before: base_column_type | s.Selector | None = None, after: base_column_type | s.Selector | None = None) -> VinylTable:
        """
        Relocate columns before or after other specified columns.
        """
    def chart(self, geoms: geom | list[Any], x: ir.Value | None, y: ir.Value | None = None, color: ir.Value | None = None, fill: ir.Value | None = None, size: ir.Value | None = None, alpha: ir.Value | None = None, facet: ir.Value | list[ir.Value] | None = None, coord_flip: bool = False, interactive: bool = True):
        """
        Visualize the table using a chart. The geoms argument should be a geom or a list of geoms. The x, y, color, fill, size, alpha, and facet arguments should be column expressions. If a list of columns is passed, the chart will be faceted by the columns in the list.

        If coord_flip is True, the x and y axes will be flipped.
        """
    def to_sql(self, dialect: str = 'duckdb', optimized: bool = False, formatted: bool = True) -> str:
        """
        Output the table as a SQL string. The dialect argument can be used to specify the SQL dialect to use.

        If optimized is True, the SQL will be optimized using the SQLglot optimizer. If formatted is True, the SQL will be formatted for readability.
        """
    def distinct(self, on: column_type_without_dict | None = None, keep: Literal['first', 'last'] | None = 'first') -> VinylTable:
        """
        Return distinct rows from the table.

        If `on` is specified, the distinct rows will be based on the columns in `on`. If it is not, the distinct rows will be based on all columns.

        If `keep` is specified, the first or last row will be kept.
        """
    def drop(self, cols: column_type_without_dict) -> VinylTable:
        """
        Remove columns from the table.
        """
    def dropna(self, on: column_type_without_dict | None = None, how: Literal['any', 'all'] = 'any') -> VinylTable:
        """
        Remove rows from the table with missing values.

        If `on` is specified, the missing values will be checked for the columns in `on`. If it is not, the missing values will be checked for all columns.

        If `how` is 'any', the row will be removed if any of the values are missing. If it is 'all', the row will be removed if all of the values are missing.
        """
    def sort(self, by: column_type | None = None) -> VinylTable:
        """
        Sort the table by the columns in `by`.

        If `by` is not specified, the table will be sorted by all columns.

        To sort a column in descending order, place a `-` in front of the column.
        """
    def limit(self, n: int | None, offset: int = 0) -> VinylTable:
        """
        Return the first `n` rows of the table, starting at the `offset` row.

        Note that the result set may not be idempotent.
        """
    def filter(self, conditions: boolean_column_type) -> VinylTable:
        """
        Filter the table based on the conditions specified. This function should be used in place of WHERE, HAVING, and QUALIFY clauses in SQL.
        """
    def filter_all(self, col_selector: column_type_all, condition_f: Callable[..., Any] | list[Callable[..., Any] | None] | None, condition_type: Literal['and', 'or'] = 'and') -> VinylTable:
        """
        Similar to other '_all' method variants, this is a generalized form of `filter` that can apply the same operation (specified in _condition_f_) to multiple columns.

        The col_selector field can be a list of column fields, where each element  `select`, and _condition_f_ should be a list of functions of the same length.

        Useful if you want to apply the same filter (e.g. value > 0) to multiple columns.

        Conditions are evaluated together using the condition_type argument. If condition_type is 'and', all conditions must be met. If condition_type is 'or', any condition can be met. If you'd like to use a mix of 'and' and 'or' conditions, call the `filter` function multiple times.
        """
    def count(self, where: base_boolean_column_type | None = None, distinct: bool = False, as_scalar: bool = False) -> VinylTable:
        """
        Return the count of rows in the table.

        If `where` is specified, the count will be based on the rows that meet the condition. If it is not, the count will be based on all rows.

        If `distinct` is True, the count will be based on distinct rows.

        If `as_scalar` is True, the result will be returned as a scalar. If it is False, the result will be returned as a table. By default, a table is returned.
        """
    def pivot(self, colnames_from: str | list[str], values_from: str | list[str], values_fill: Callable[..., Any] | None = None, values_agg: Callable[[ir.Value], ir.Scalar] = ..., colnames_sep: str = '_', colnames_sort: bool = False, colnames_prefix: str = '', id_cols: str | list[str] | None = None):
        """
        Pivot a table to a wider format.

        <u>Argument descriptions</u>
        *colnames_from*: The columns to use as the names of the new columns
        *colnames_sep*: The separator to use when combining the colnames_from columns, if more than one is specified
        *colnames_prefix*: The prefix to use for the new columns
        *colnames_sort*: Whether to sort the names of the new columns. If False, the names will be sorted in the order they are found in the table.
        *values_from*: The columns to use as the values of the new columns
        *values_fill*: The fill value to use for missing values in the new columns. Defaults to null
        *values_agg*: The aggregation function to use for the new columns. Defaults to the first value.
        *id_cols*: The columns that uniquely specify each row. If None, all columns not specified in colnames_from or values_from will be used.

        """
    def unpivot(self, cols: str | list[str], colnames_to: str = 'name', colnames_transform: Callable[..., ir.Value] | None = None, values_to: str = 'value', values_transform: Callable[..., ir.Value] | None = None) -> VinylTable:
        """
        Transform a table from wider to longer.

        <u>Argument descriptions</u>
        *cols*: The column names to unpivot
        *colnames_to*: The name of the new column to store the names of the original columns
        *colnames_transform*: A function to transform the names of the original columns to be stored in the `names_to` column
        *values_to*: The name of the new column to store the values of the original columns
        *values_transform*: A function to transform the values of the original columns to be stored in the `values_to` column

        """
    def schema(self) -> VinylSchema:
        """
        Return the schema of the table.
        """
    def get_name(self) -> str:
        """
        Return the name of the table.
        """
    @property
    def columns(self) -> list[str]:
        """
        Return the column names of the table.
        """
    def sample(self, fraction: float, method: Literal['row', 'block']) -> VinylTable:
        """
        Sample a fraction of rows from a table. Results may not be idempotent.

        See specific note from Ibis below:

        Sampling is by definition a random operation. Some backends support specifying a seed for repeatable results, but not all backends support that option. And some backends (duckdb, for example) do support specifying a seed but may still not have repeatable results in all cases.
        In all cases, results are backend-specific. An execution against one backend is unlikely to sample the same rows when executed against a different backend, even with the same seed set.
        """
    def eda(self, cols: column_type | None = None, topk: int = 3) -> VinylTable:
        """
        Return summary statistics for each column in the table.

        If cols is specified, the summary statistics will be returned for the columns in cols. If it is not, the summary statistics will be returned for all columns.
        """
    def metric(self, cols: ir.Scalar | Callable[..., ir.Scalar] | list[ir.Scalar | Callable[..., ir.Scalar]] | dict[str, ir.Scalar | Callable[..., ir.Scalar]], ts: ir.TimestampValue | Callable[..., ir.TimestampValue], by: ir.Value | Callable[..., ir.Value] | Sequence[ir.Value | Callable[..., ir.Value]] = [], fill: FillOptions | Callable[..., Any] = ...) -> MetricStore:
        """
        Create a MetricStore (dynamic table) with a set of metrics based on the table. `cols` are the metrics, `ts` is the timestamp, `by` are the dimensions, and `fill` is the fill strategy for missing values.

        Note that this is an immutable operation, so you must assign the result to a variable to use it.

        To access the data stored in the MetricStore, use the `select` method.
        """
    @classmethod
    def from_memory(cls, data: pd.DataFrame | pl.DataFrame | pa.Table):
        """
        Create a VinylTable from a pandas, polars, or pyarrow object
        """
    @classmethod
    def from_file(cls, path: str):
        """
        Create a VinylTable from a csv, json, or parquet file
        """
