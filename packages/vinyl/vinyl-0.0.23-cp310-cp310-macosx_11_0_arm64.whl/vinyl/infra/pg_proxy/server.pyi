import duckdb
from _typeshed import Incomplete
from typing import Tuple
from vinyl.infra.pg_proxy.backends.duckdb import DuckDBConnection as DuckDBConnection
from vinyl.infra.pg_proxy.bv_dialects import BVDuckDB as BVDuckDB, BVPostgres as BVPostgres
from vinyl.infra.pg_proxy.postgres import ProxyServer as ProxyServer
from vinyl.infra.pg_proxy.rewrite import Rewriter as Rewriter

class TurntableMetricsRewriter(Rewriter):
    def rewrite(self, sql: str) -> str: ...

rewriter: Incomplete

def create(db: duckdb.DuckDBPyConnection, host_addr: Tuple[str, int], auth: dict = None) -> ProxyServer: ...
