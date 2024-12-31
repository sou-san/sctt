from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Label, Static
from textual_pyfiglet.pyfiglet import figlet_format

from sctt.modules.timer import Timer
from sctt.screens.dialog_screen import DialogScreen
from sctt.widgets.my_vertical_scroll import MyVerticalScroll


class SolveTime(Static):
    styled_time: reactive[str] = reactive("", init=False)
    penalty: reactive[str] = reactive("", init=False)

    def __init__(self, time: float) -> None:
        super().__init__()
        self.time: float = time

    def on_mount(self) -> None:
        self.style_time(self.penalty)

    def style_time(self, penalty: str) -> None:
        time: str
        font: str = "small"

        match penalty:
            case "":
                time = Timer.format_time(self.time, 2)
                self.styled_time = figlet_format(time, font)
            case "plus_2":
                time = Timer.format_time(self.time + 2, 2)
                self.styled_time = figlet_format(f"{time}+", font)
            case "dnf":
                time = Timer.format_time(self.time, 2)
                self.styled_time = figlet_format(f"DNF ({time})", font)
            case _:
                raise ValueError

    def watch_styled_time(self, styled_time: str) -> None:
        self.update(styled_time)

    def watch_penalty(self, penalty: str) -> None:
        self.style_time(penalty)


class Buttons(Horizontal):
    pass


class SolveData(Vertical):
    pass


class Body(Vertical):
    pass


class SolveScreen(ModalScreen[str]):
    BINDINGS = [
        ("escape", "close_solve_screen", "Close"),
        ("o", "ok_penalty", "OK"),
        ("2", "plus_2_penalty", "+2"),
        ("d", "dnf_penalty", "DNF"),
        ("x", "remove_solve", "Remove"),
    ]

    def __init__(
        self, solve_id: int, event: str, time: float, penalty: str, scramble: str, date: str
    ) -> None:
        super().__init__()
        self.solve_id: int = solve_id
        self.event: str = event
        self.time: float = time
        self.penalty: str = penalty
        self.scramble: str = scramble
        self.date: str = date

        self.result: str | None = None

    def compose(self) -> ComposeResult:
        with Body():
            with Center():
                yield SolveTime(self.time)
            with Center():
                with Buttons():
                    yield Button("OK", id="ok")
                    yield Button("+2", id="plus_2")
                    yield Button("DNF", id="dnf")
                    yield Label()  # separator
                    yield Button("X", id="remove")
            with Center():
                with SolveData():
                    with Horizontal():
                        yield Label("Event: ", classes="label")
                        yield Label(self.event, classes="value")
                    with Horizontal(classes="middle"):
                        yield Label("Scramble: ", classes="label")
                        with MyVerticalScroll(classes="value"):
                            yield Label(self.scramble)
                    with Horizontal():
                        yield Label("Date: ", classes="label")
                        yield Label(self.date, classes="value")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Vertical).border_title = "time"
        self.query_one(SolveTime).penalty = self.penalty

    def handle_selection(self, result: str | None) -> None:
        self.result = result

        match self.result:
            case "ok":
                self.query_one(SolveTime).penalty = ""
            case "plus_2":
                self.query_one(SolveTime).penalty = "plus_2"
            case "dnf":
                self.query_one(SolveTime).penalty = "dnf"
            case "remove":

                def check_result(result: str | None) -> None:
                    match result:
                        case "ok":
                            self.action_close_solve_screen()
                        case _:
                            self.result = None

                self.app.push_screen(
                    DialogScreen("Are you sure you want to remove this solve?"), check_result
                )
            case _:
                self.result = None

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        self.handle_selection(event.button.id)

    def action_ok_penalty(self) -> None:
        self.query_one("#ok", Button).focus()
        self.handle_selection("ok")

    def action_plus_2_penalty(self) -> None:
        self.query_one("#plus_2", Button).focus()
        self.handle_selection("plus_2")

    def action_dnf_penalty(self) -> None:
        self.query_one("#dnf", Button).focus()
        self.handle_selection("dnf")

    def action_remove_solve(self) -> None:
        self.query_one("#remove", Button).focus()
        self.handle_selection("remove")

    def action_close_solve_screen(self) -> None:
        self.dismiss(self.result)
