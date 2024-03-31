from _typeshed import Incomplete
from fastapi import FastAPI, Request as Request
from vinyl.lib.project import Project as Project
from vinyl.lib.query_engine import QueryEngine as QueryEngine

class ProjectDependency:
    project: Incomplete
    def __init__(self, project: Project) -> None: ...

async def lifespan(app: FastAPI): ...
def get_project(request: Request): ...

app: Incomplete
