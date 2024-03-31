import typer
from .preview import preview_cli as preview_cli
from .project import project_cli as project_cli
from .sources import sources_cli as sources_cli
from vinyl.cli.events import Event as Event, EventLogger as EventLogger
from vinyl.cli.user import DEFAULT_CREDS_PATH as DEFAULT_CREDS_PATH

CLERK_CLIENT_ID: str
app: typer.Typer

def main(ctx: typer.Context, version: bool = ...): ...
async def listen_for_event(state, stop_event) -> None: ...
def login() -> None:
    """Log into Turntable"""
def init_project(project_name: str):
    """Initialize a new Vinyl project and it's file strucutre"""
