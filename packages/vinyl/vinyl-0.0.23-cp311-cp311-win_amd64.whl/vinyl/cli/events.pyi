from _typeshed import Incomplete
from enum import Enum
from vinyl.cli.user import User as User

class Event(Enum):
    LOGIN: str
    SOURCE_GEN: str
    PROJECT_INIT: str
    PREVIEW_MODEL: str
    PREVIEW_METRIC: str
    DEPLOY: str
    SERVE: str

class EventLogger:
    user: Incomplete
    posthog: Incomplete
    def __init__(self) -> None: ...
    def log_event(self, event: Event): ...
