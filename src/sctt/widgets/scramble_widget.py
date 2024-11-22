from enum import Enum, auto
from typing import Iterable

from rich.console import RenderableType
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.types import SelectType
from textual.widgets import Select, Static
from textual.widgets._select import SelectOverlay

from sctt.modules.scramble import generate_scramble
from sctt.screens.input_scramble_screen import InputScrambleScreen
from sctt.version import SCTT_VERSION
from sctt.widgets.my_vertical_scroll import MyVerticalScroll


class ScrambleMode(Enum):
    GENERATE = auto()
    INPUT = auto()


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
    SCRAMBLE_OPTIONS: list[tuple[str, ScrambleMode]] = [
        ("Gen", ScrambleMode.GENERATE),
        ("Input", ScrambleMode.INPUT),
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
        yield MySelect[ScrambleMode](
            self.SCRAMBLE_OPTIONS, allow_blank=False, id="scramble_options"
        )
        yield MySelect[int](self.CUBE_SIZE_OPTIONS, allow_blank=False)


class ScrambleDisplay(Static):
    pass


class ScrambleWidget(Horizontal):
    scramble: reactive[str] = reactive("", init=False)

    class Changed(Message):
        def __init__(self, scramble: str, cube_size: int) -> None:
            super().__init__()
            self.scramble: str = scramble
            self.cube_size: int = cube_size

    def compose(self) -> ComposeResult:
        yield ScrambleSettingsSelect()
        with MyVerticalScroll():
            yield ScrambleDisplay()

    def on_mount(self) -> None:
        self.cube_size: int = 3
        self.query_one(VerticalScroll).border_title = f"sctt v{SCTT_VERSION}"

    def watch_scramble(self, scramble: str) -> None:
        self.query_one(ScrambleDisplay).update(scramble)
        self.post_message(self.Changed(scramble, self.cube_size))

    def set_inputted_scramble(self, scramble: str | None) -> None:
        if scramble is None:
            self.scramble_mode = ScrambleMode.GENERATE
            self.query_one(MySelect[ScrambleMode]).set_options(
                self.query_one(ScrambleSettingsSelect).SCRAMBLE_OPTIONS
            )
            self.update()
        else:
            self.scramble_mode = ScrambleMode.INPUT
            self.scramble = scramble.strip()

    def update(self) -> None:
        match self.scramble_mode:
            case ScrambleMode.GENERATE:
                match self.cube_size:
                    case 2 | 3 | 4 | 5 | 6 | 7:
                        self.scramble = generate_scramble(self.cube_size)
                    case _:
                        pass
            case ScrambleMode.INPUT:
                self.app.push_screen(InputScrambleScreen(), self.set_inputted_scramble)

    @on(MySelect.Changed)
    def handle_my_select_changed(self, event: MySelect.Changed) -> None:
        match event.value:
            case ScrambleMode.GENERATE:
                self.scramble_mode = ScrambleMode.GENERATE
                self.update()
            case ScrambleMode.INPUT:
                self.scramble_mode = ScrambleMode.INPUT
                self.update()
            case 2 | 3 | 4 | 5 | 6 | 7:
                self.cube_size = event.value
                self.update()
            case _:
                pass
