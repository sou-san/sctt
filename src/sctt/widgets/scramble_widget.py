from enum import StrEnum

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from sctt.modules.scramble import generate_scramble
from sctt.screens.input_scramble_screen import InputScrambleScreen
from sctt.version import SCTT_VERSION
from sctt.widgets.my_select import MySelect
from sctt.widgets.my_vertical_scroll import MyVerticalScroll


class ScrambleMode(StrEnum):
    GENERATE = "Generate"
    INPUT = "Input"


class SolveEvent(StrEnum):
    THREE = "3x3x3"  # Default value
    TWO = "2x2x2"
    FOUR = "4x4x4"
    FIVE = "5x5x5"
    SIX = "6x6x6"
    SEVEN = "7x7x7"
    THREE_OH = "3x3x3 oh"  # One-Handed
    THREE_FM = "3x3x3 fm"  # Fewest Moves
    THREE_BLD = "3x3x3 bld"  # Blindfolded
    FOUR_BLD = "4x4x4 bld"  # Blindfolded
    FIVE_BLD = "5x5x5 bld"  # Blindfolded


class ScrambleSettingsSelect(Vertical):
    SCRAMBLE_MODE_OPTIONS: list[tuple[ScrambleMode, ScrambleMode]] = [
        (mode, mode) for mode in ScrambleMode
    ]
    SOLVE_EVENT_OPTIONS: list[tuple[SolveEvent, SolveEvent]] = [
        (event, event) for event in SolveEvent
    ]

    def compose(self) -> ComposeResult:
        yield MySelect(self.SCRAMBLE_MODE_OPTIONS, allow_blank=False, id="scramble_options")
        yield MySelect(self.SOLVE_EVENT_OPTIONS, allow_blank=False)


class ScrambleDisplay(Static):
    pass


class ScrambleWidget(Horizontal):
    scramble: reactive[str] = reactive("", init=False, always_update=True)

    class Changed(Message):
        def __init__(self, scramble: str, solve_event: SolveEvent) -> None:
            super().__init__()
            self.scramble: str = scramble
            self.solve_event: SolveEvent = solve_event

    @staticmethod
    def get_cube_size(solve_event: SolveEvent) -> int:
        return int(solve_event[0])

    def compose(self) -> ComposeResult:
        yield ScrambleSettingsSelect()
        with MyVerticalScroll():
            yield ScrambleDisplay()

    def on_mount(self) -> None:
        self.solve_event: SolveEvent = SolveEvent.THREE
        self.query_one(VerticalScroll).border_title = f"sctt v{SCTT_VERSION}"

    def watch_scramble(self, scramble: str) -> None:
        self.query_one(ScrambleDisplay).update(scramble)
        self.post_message(self.Changed(scramble, self.solve_event))

    def update(self) -> None:
        def _check_scramble(scramble: str | None) -> None:
            if scramble is None:
                select = self.query_one(MySelect[ScrambleMode])
                select.value = self.scramble_mode = ScrambleMode.GENERATE
                self.update()
            else:
                self.scramble = scramble.strip()

        match self.scramble_mode:
            case ScrambleMode.GENERATE:
                self.scramble = generate_scramble(self.get_cube_size(self.solve_event))
            case ScrambleMode.INPUT:
                self.app.push_screen(InputScrambleScreen(), _check_scramble)

    @on(MySelect.Changed)
    def handle_my_select_changed(self, event: MySelect.Changed) -> None:
        match event.value:
            case ScrambleMode():
                self.scramble_mode = event.value
            case SolveEvent():
                self.solve_event = event.value
            case _:
                raise ValueError(f"Invalid selected value: {event.value}")

        self.update()
