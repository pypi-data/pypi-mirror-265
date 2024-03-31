from ibis import Schema as Schema
from textual.app import App

def rich_print(*args, **kwargs) -> None: ...

class TurntableTextualApp(App):
    def action_reload(self) -> None: ...
