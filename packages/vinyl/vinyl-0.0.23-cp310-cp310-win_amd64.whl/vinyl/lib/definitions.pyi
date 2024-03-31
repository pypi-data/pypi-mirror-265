import dataclasses
from typing import Any

@dataclasses.dataclass
class Defs:
    resources: list[Any]
    sources: list[Any]
    models: list[Any]
    metrics: list[Any]
    def __init__(self, resources, sources, models, metrics) -> None: ...

def load_defs() -> Defs: ...
