import typer
from textual.app import ComposeResult as ComposeResult
from vinyl import Field as Field
from vinyl.cli.events import Event as Event, EventLogger as EventLogger
from vinyl.lib.constants import PreviewHelper as PreviewHelper
from vinyl.lib.erd import create_erd_app as create_erd_app
from vinyl.lib.project import Project as Project
from vinyl.lib.query_engine import QueryEngine as QueryEngine
from vinyl.lib.utils.graphics import TurntableTextualApp as TurntableTextualApp

preview_cli: typer.Typer

class PreviewTable(TurntableTextualApp):
    def __init__(self, rows, columns) -> None: ...
    def compose(self) -> ComposeResult: ...
    def on_mount(self) -> None: ...

def preview_model(name: str = ..., twin: bool = ..., limit: int = ...):
    """Preview a model"""
def preview_metric(name: str = ..., grain: str = ..., dims: list[str] = ..., cols: list[str] = ...):
    """Preview a model"""
def erd(names: list[str] = ...):
    """Generate an ERD"""
