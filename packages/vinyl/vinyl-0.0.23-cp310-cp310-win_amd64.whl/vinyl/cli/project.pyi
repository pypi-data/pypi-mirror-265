import typer
from vinyl.cli.events import Event as Event, EventLogger as EventLogger
from vinyl.lib.metric import MetricStore as MetricStore
from vinyl.lib.project import Project as Project

project_cli: typer.Typer

def deploy() -> None:
    """Deploy a Vinyl project"""
def proxy_server(db_path, bv_host, bv_port) -> None: ...
def run_pg_proxy(db_path, bv_host, bv_port): ...
def http_server() -> None: ...
def run_fast_api_process(): ...
def serve() -> None:
    """Serve a Vinyl project"""
