import abc
from abc import ABC
from dataclasses import dataclass
from ibis import Schema as Schema
from ibis.backends import BaseBackend as BaseBackend

@dataclass
class SourceInfo:
    def __init__(self, _name, _location, _schema, _parent_resource) -> None: ...

class _ResourceConnector(ABC, metaclass=abc.ABCMeta):
    """Base interface for handling connecting to resource and getting sources"""

class _TableConnector(_ResourceConnector, metaclass=abc.ABCMeta):
    def __init__(self, path: str) -> None: ...

class _DatabaseConnector(_ResourceConnector, metaclass=abc.ABCMeta): ...

class _FileConnector(_ResourceConnector, metaclass=abc.ABCMeta):
    def __init__(self, path: str) -> None: ...

class DatabaseFileConnector(_FileConnector, _DatabaseConnector):
    def __init__(self, path: str, tables: list[str] = ['*.*.*'], use_sqlite: bool = False) -> None: ...

class FileConnector(_FileConnector, _TableConnector):
    def __init__(self, path: str) -> None: ...

class BigQueryConnector(_DatabaseConnector):
    def __init__(self, tables: list[str], service_account_path: str | None = None, service_account_info: str | None = None) -> None: ...

class PostgresConnector(_DatabaseConnector):
    def __init__(self, host: str, port: int, user: str, password: str, tables: list[str]) -> None: ...
