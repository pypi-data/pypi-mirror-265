from _typeshed import Incomplete
from enum import Enum
from lets_plot.plot.core import LayerSpec as LayerSpec
from typing import Any, Callable
from vinyl.lib.column_methods import ColumnBuilder as ColumnBuilder, ColumnListBuilder as ColumnListBuilder, base_column_type as base_column_type, column_type_without_dict as column_type_without_dict
from vinyl.lib.settings import PyProjectSettings as PyProjectSettings

class geom(Enum):
    scatter: Callable[..., LayerSpec]
    line: Callable[..., LayerSpec]
    bar: Callable[..., LayerSpec]
    area: Callable[..., LayerSpec]
    stacked_bar: Callable[..., LayerSpec]
    percent_bar: Callable[..., LayerSpec]
    histogram: Callable[..., LayerSpec]
    histogram_2d: Callable[..., LayerSpec]
    violin: Callable[..., LayerSpec]
    boxplot: Callable[..., LayerSpec]
    density: Callable[..., LayerSpec]
    ridge: Callable[..., LayerSpec]
    trendline_lm: Callable[..., LayerSpec]
    trendline_loess: Callable[..., LayerSpec]

class BaseChart:
    x: base_column_type
    y: base_column_type | None
    color: base_column_type | None
    fill: base_column_type | None
    size: base_column_type | None
    alpha: base_column_type | None
    facet: column_type_without_dict | None
    coord_flip: Incomplete
    def __init__(self, geoms: geom | list[geom], source: Any, x: base_column_type, y: base_column_type | None = None, color: base_column_type | None = None, fill: base_column_type | None = None, size: base_column_type | None = None, alpha: base_column_type | None = None, facet: column_type_without_dict | None = None, coord_flip: bool = False) -> None: ...
