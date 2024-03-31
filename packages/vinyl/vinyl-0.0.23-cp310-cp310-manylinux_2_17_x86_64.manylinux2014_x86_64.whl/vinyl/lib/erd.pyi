import networkx as nx
from _typeshed import Incomplete
from collections.abc import Hashable
from netext.geometry.point import FloatPoint
from netext.layout_engines.engine import G, LayoutEngine
from netext.textual.widget import GraphView
from textual.app import ComposeResult as ComposeResult
from vinyl.lib.utils.graphics import TurntableTextualApp as TurntableTextualApp

class GrandalfView:
    w: int
    h: int
    xy: Incomplete

class GrandalfLRSugiyamaLayout(LayoutEngine[G]):
    """Layout engine that uses the grandalf library to layout the graph using the Sugiyama algorithm.

    Multiple components will be placed next to each other.
    """
    def __call__(self, g: G) -> dict[Hashable, FloatPoint]: ...

def create_erd_app(g: nx.DiGraph) -> GraphView: ...
