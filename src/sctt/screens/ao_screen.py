from typing import Any

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Label
from textual_pyfiglet.pyfiglet import figlet_format

from sctt.modules.timer import Timer
from sctt.widgets.my_datatable import MyDataTable


class AOScreen(ModalScreen[None]):
    BINDINGS = [
        ("escape", "dismiss", "Close"),
    ]

    def __init__(self, solves: list[tuple[Any, ...]], ao_value: Text) -> None:
        self.num_ao = len(solves)
        self.solves: list[tuple[Any, ...]] = solves
        self.ao_value: Text = ao_value
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label()
            with Center():
                yield MyDataTable[str]()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Vertical).border_title = f"ao{self.num_ao}"

        table = self.query_one(MyDataTable[str])
        table.cursor_type = "none"
        table.zebra_stripes = True

        table.add_columns("no.", "event", "time", "scramble", "date")

        for i, solve in enumerate(self.solves, start=1):
            table.add_row(
                str(i),
                str(solve[1]),
                self.format_apply_penalty(solve[2], solve[3]),
                str(solve[4]),
                str(solve[5]),
            )

        self.query_one(Label).update(figlet_format(str(self.ao_value), "small"))

    def format_apply_penalty(self, time: int, penalty: str) -> str:
        match penalty:
            case "":
                return Timer.format_time(time, 2)
            case "plus_2":
                return f"{Timer.format_time(time + 2, 2)}+"
            case "dnf":
                return "DNF"
            case _:
                raise ValueError(f"Invalid penalty: {penalty}")
