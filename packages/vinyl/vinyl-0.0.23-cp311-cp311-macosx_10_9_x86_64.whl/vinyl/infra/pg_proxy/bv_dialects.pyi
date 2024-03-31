from _typeshed import Incomplete
from sqlglot import exp
from sqlglot.dialects import DuckDB, Postgres, Trino

class ToISO8601(exp.Func): ...
class BVPostgres(Postgres): ...

class BVTrino(Trino):
    class Tokenizer(Trino.Tokenizer):
        KEYWORDS: Incomplete
    class Parser(Trino.Parser):
        FUNCTIONS: Incomplete

class BVDuckDB(DuckDB):
    class Generator(DuckDB.Generator):
        TRANSFORMS: Incomplete
