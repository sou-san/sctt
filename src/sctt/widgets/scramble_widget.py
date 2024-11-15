from typing import Iterable

from rich.console import RenderableType
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.types import SelectType
from textual.widgets import Select, Static
from textual.widgets._select import SelectOverlay

from sctt.modules.scramble import generate_scramble


class MySelect(Select[SelectType], inherit_bindings=False):
    BINDINGS = [
        Binding("enter", "show_overlay", "Show Overlay", show=False),
        Binding("up,k", "cursor_up", "Cursor Up", show=False),
        Binding("down,j", "cursor_down", "Cursor Down", show=False),
    ]

    def __init__(
        self,
        options: Iterable[tuple[RenderableType, SelectType]],
        *,
        allow_blank: bool = True,
        id: str | None = None,
    ) -> None:
        super().__init__(options=options, allow_blank=allow_blank, id=id)

    def action_cursor_up(self) -> None:
        self.query_one(SelectOverlay).action_cursor_up()

    def action_cursor_down(self) -> None:
        self.query_one(SelectOverlay).action_cursor_down()


class ScrambleSettingsSelect(Vertical):
    SCRAMBLE_OPTOINS: list[tuple[str, str]] = [
        ("Gen", "generate"),
        # TODO: スクランブルを入力できるようにする。
        # ("Input", "input"),
    ]

    CUBE_SIZE_OPTIONS: list[tuple[str, int]] = [
        ("3x3x3", 3),  # Default value
        ("2x2x2", 2),
        ("4x4x4", 4),
        ("5x5x5", 5),
        ("6x6x6", 6),
        ("7x7x7", 7),
    ]

    def compose(self) -> ComposeResult:
        yield MySelect[str](self.SCRAMBLE_OPTOINS, allow_blank=False, id="scramble_options")
        yield MySelect[int](self.CUBE_SIZE_OPTIONS, allow_blank=False)


class ScrambleDisplay(Static):
    pass


class ScrambleWidget(Horizontal):
    class Changed(Message):
        def __init__(self, scramble: str, cube_size: int) -> None:
            super().__init__()
            self.scramble: str = scramble
            self.cube_size: int = cube_size

    def compose(self) -> ComposeResult:
        yield ScrambleSettingsSelect()
        with VerticalScroll():
            yield ScrambleDisplay()

    def update_scramble(self) -> None:
        match self.cube_size:
            case 2 | 3 | 4 | 5 | 6 | 7:
                self.scramble: str = generate_scramble(self.cube_size)
                self.query_one(ScrambleDisplay).update(self.scramble)
                self.post_message(self.Changed(self.scramble, self.cube_size))
            case _:
                pass

    @on(MySelect.Changed)
    def handle_my_select_changed(self, event: MySelect.Changed) -> None:
        match event.value:
            case 2 | 3 | 4 | 5 | 6 | 7:
                self.cube_size = event.value
                self.update_scramble()
            case _:
                pass
