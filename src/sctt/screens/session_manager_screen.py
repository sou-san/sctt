from math import isnan
from typing import Any

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Input, Label
from textual.widgets.data_table import RowDoesNotExist

from sctt.modules.database import Database
from sctt.modules.timer import Timer
from sctt.screens.dialog_screen import DialogScreen
from sctt.widgets.my_datatable import MyDataTable


class Body(Vertical):
    pass


class InputSessionScreen(ModalScreen[str]):
    BINDINGS = [("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        with Body():
            yield Label("Enter session name")
            yield Input()

    def on_mount(self) -> None:
        self.session_name: str = ""

    @on(Input.Changed)
    def handle_input_changed(self, event: Input.Changed) -> None:
        self.session_name = event.value

    @on(Input.Submitted)
    def handle_input_submit(self) -> None:
        self.dismiss(self.session_name)


class SessionManagerScreen(ModalScreen[int]):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("c", "create_session", "Create"),
        Binding("x", "delete_session", "Delete"),
        Binding("r", "rename_session", "Rename"),
    ]

    def __init__(self, database: Database, current_session_id: int) -> None:
        super().__init__()
        self.db: Database = database
        self.current_session_id: int = current_session_id

    def compose(self) -> ComposeResult:
        with Body():
            with Center():
                yield Label("Session Manager")
            with Center():
                yield MyDataTable[Text]()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(MyDataTable[Text])
        table.cursor_type = "row"
        table.zebra_stripes = True

        table.add_column("name", key="name")
        table.add_column("solve", key="solve")
        table.add_column("mean", key="mean")
        table.add_column("created_at", key="created_at")
        table.add_column("updated_at", key="updated_at")

        for session in self.db.get_all_sessions():
            self.add_session_to_table(session)

        table.move_cursor(row=table.get_row_index(str(self.current_session_id)))

    def add_session_to_table(self, session: tuple[Any, ...]) -> None:
        session_id, name, created_at, updated_at = session
        mean: float = self.db.calculate_solve_mean(session_id)

        self.query_one(MyDataTable[Text]).add_row(
            Text(name, justify="center"),
            Text(str(self.db.get_solve_count(session_id)), justify="center"),
            Text(
                "-" if isnan(mean) else Timer.format_time(mean, 2),
                justify="center",
            ),
            Text(created_at, justify="center"),
            Text(updated_at, justify="center"),
            key=str(session_id),
        )

    def action_create_session(self) -> None:
        def handle_result(result: str | None) -> None:
            if result:
                session_id: int | None = self.db.create_session(result)

                if session_id is None:
                    raise ValueError("Failed to create session.")

                self.add_session_to_table(self.db.get_session(session_id))

        self.app.push_screen(InputSessionScreen(), handle_result)

    def action_delete_session(self) -> None:
        def handle_result(result: str | None) -> None:
            if result == "ok":
                self.db.delete_session(self.session_id)

                try:
                    self.query_one(MyDataTable[str]).remove_row(str(self.session_id))
                except RowDoesNotExist:
                    # 削除するために x を連打したとき、RowDoesNotExist が発生する。
                    # 一度、カーソルを移動して再度、先ほど RowDoesNotExist が発生した行を選択すると RowDoesNotExist は発生しなくなる。
                    # これは textual のバグのような気がする。
                    pass

                if not self.db.get_all_sessions():
                    session_id: int | None = self.db.create_session("session 1")

                    if session_id is None:
                        raise ValueError("Failed to create session.")

                    self.dismiss(session_id)
                elif self.session_id == self.current_session_id:
                    self.dismiss(self.db.get_all_sessions()[0][0])

        self.app.push_screen(
            DialogScreen("Are you sure you want to delete this session?"), handle_result
        )

    def action_rename_session(self) -> None:
        def handle_result(result: str | None) -> None:
            if result:
                self.db.rename_session(result, self.session_id)
                self.query_one(MyDataTable[str]).update_cell(
                    str(self.session_id), "name", result, update_width=True
                )

        self.app.push_screen(InputSessionScreen(), handle_result)

    @on(MyDataTable.RowSelected)
    def switch_session(self) -> None:
        self.dismiss(self.session_id)

    @on(MyDataTable.RowHighlighted)
    def handle_row_selected(self, event: MyDataTable.RowHighlighted) -> None:
        if event.row_key.value is not None:
            self.session_id = int(event.row_key.value)
        else:
            raise ValueError(f"Invalid session_id: {event.row_key.value}")
