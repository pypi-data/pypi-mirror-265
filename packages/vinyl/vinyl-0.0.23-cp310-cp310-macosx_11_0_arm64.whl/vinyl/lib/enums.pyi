from enum import Enum

class FillOptions(Enum):
    null: str
    previous: str
    next: str

class WindowType(Enum):
    rows: str
    range: str

class AssetType(Enum):
    MODEL: str
    METRIC: str
