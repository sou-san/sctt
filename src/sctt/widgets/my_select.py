from collections.abc import Iterable

from rich.console import RenderableType
from textual.binding import Binding
from textual.types import SelectType
from textual.widgets import Select
from textual.widgets._select import SelectOverlay


class MySelect(Select[SelectType], inherit_bindings=False):
    """Vim キーバインドが使える Select"""

    BINDINGS = [
        Binding("enter", "show_overlay", "Show Overlay", show=False),
        Binding("up,k", "cursor_up", "Cursor Up", show=False),
        Binding("down,j", "cursor_down", "Cursor Down", show=False),
    ]
    """
    | Key(s) | Description |
    | :- | :- |
    | enter,down,j,space,up,k | Activate the overlay |
    """

    def __init__(
        self,
        options: Iterable[tuple[RenderableType, SelectType]],
        *,
        allow_blank: bool = True,
        type_to_search: bool = False,
        id: str | None = None,
    ) -> None:
        super().__init__(
            options=options, allow_blank=allow_blank, type_to_search=type_to_search, id=id
        )

    def action_cursor_up(self) -> None:
        self.query_one(SelectOverlay).action_cursor_up()

    def action_cursor_down(self) -> None:
        self.query_one(SelectOverlay).action_cursor_down()
