from typing import Any, Callable
from vinyl.lib.connect import DatabaseFileConnector as DatabaseFileConnector
from vinyl.lib.constants import PreviewHelper as PreviewHelper
from vinyl.lib.field import Field as Field
from vinyl.lib.table import VinylTable as VinylTable

def source(resource: Callable[..., Any], sample_row_count: int | None = 1000): ...
