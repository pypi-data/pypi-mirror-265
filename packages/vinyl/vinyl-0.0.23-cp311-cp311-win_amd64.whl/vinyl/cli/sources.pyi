from _typeshed import Incomplete
from vinyl.cli.events import Event as Event, EventLogger as EventLogger
from vinyl.lib.connect import DatabaseFileConnector as DatabaseFileConnector, SourceInfo as SourceInfo
from vinyl.lib.project import Project as Project
from vinyl.lib.utils.obj import is_valid_class_name as is_valid_class_name, table_to_python_class as table_to_python_class, to_valid_class_name as to_valid_class_name

console: Incomplete
sources_cli: Incomplete

def list_sources(tables: bool = False):
    """Caches sources to a local directory (default: .turntable/sources)"""
def source_to_class_string(source: SourceInfo, saved_attributes: dict[str, str], generate_twin: bool = False, root_path: str | None = None, sample_size: int = 1000) -> str: ...
def generate_sources(twin: bool = ..., resources: list[str] = ...):
    """Generates schema files for sources"""
