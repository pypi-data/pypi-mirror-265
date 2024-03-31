import dataclasses
import ibis.expr.types as ir
from typing import Any, Callable
from vinyl.lib.connect import SourceInfo as SourceInfo, _ResourceConnector
from vinyl.lib.metric import MetricStore as MetricStore
from vinyl.lib.table import VinylTable as VinylTable

@dataclasses.dataclass
class Resource:
    name: str
    connector: _ResourceConnector
    def_: Any
    def __init__(self, name, connector, def_) -> None: ...

class Project:
    resources: list[Resource]
    sources: list[ir.Table]
    models: list[Callable[..., Any]]
    metrics: list[Callable[..., Any]]
    def __init__(self, resources: list[Callable[..., Any]], sources: list[ir.Table] | None = None, models: list[Callable[..., Any]] | None = None, metrics: list[Callable[..., Any]] | None = None) -> None: ...
