from pathlib import Path

import keyboard
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Resize
from textual.widgets import Footer

from sctt.locations import get_cache_file
from sctt.modules.database import Database
from sctt.screens.blocking_screen import MIN_HEIGHT, MIN_WIDTH, BlockingScreen
from sctt.widgets.cube_net_widget import CubeNetWidget
from sctt.widgets.scramble_widget import ScrambleWidget
from sctt.widgets.stats_widget import StatsWidget
from sctt.widgets.timer_widget import TimerWidget


def get_last_session_id() -> int:
    with open(get_cache_file(), "r") as f:
        return int(f.readline())


def save_last_session_id(session_id: int) -> None:
    with open(get_cache_file(), "w") as f:
        f.write(str(session_id))


class SolveBuffer:
    event: str
    time: float
    penalty: str
    scramble: str
    session_id: int


class AppBody(Vertical):
    pass


class Sctt(App[None]):
    CSS_PATH = Path(__file__).parent / "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "", "Start / Stop"),  # Dummy key binding for the keyboard lib.
    ]

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db: Database = db
        self.solve_buffer: SolveBuffer = SolveBuffer()

        if not self.db.get_all_sessions():
            session_id: int | None = self.db.create_session("session 1")

            if session_id is None:
                raise ValueError("Failed to create session.")
            else:
                save_last_session_id(session_id)
        else:
            session_id = get_last_session_id()

        self.solve_buffer.session_id = session_id

    def compose(self) -> ComposeResult:
        with AppBody():
            with Horizontal():
                self.stats_widget = StatsWidget()
                yield self.stats_widget
                with Vertical():
                    yield ScrambleWidget()
                    self.timer_widget = TimerWidget()
                    yield self.timer_widget
                    self.cube_net_widget = CubeNetWidget()
                    yield self.cube_net_widget
            yield Footer()

    def on_mount(self) -> None:
        self.stats_widget.update(
            self.db.get_solve_ids_and_times_and_penalties(self.solve_buffer.session_id)
        )

    def on_app_focus(self) -> None:
        keyboard.hook(self.timer_widget.key_events)

    def on_app_blur(self) -> None:
        keyboard.unhook_all()

    def on_resize(self, event: Resize) -> None:
        if event.size.width < MIN_WIDTH or event.size.height < MIN_HEIGHT:
            self.push_screen(BlockingScreen())

    @on(TimerWidget.Solved)
    def update_scramble(self) -> None:
        self.query_one(ScrambleWidget).update()

    def save_solve(self) -> int | None:
        solve_id: int | None = self.db.add_solve(
            self.solve_buffer.event,
            self.solve_buffer.time,
            self.solve_buffer.scramble,
            self.solve_buffer.session_id,
        )

        return solve_id

    @on(TimerWidget.Solved)
    def update_stats(self, message: TimerWidget.Solved) -> None:
        self.solve_buffer.time = message.time_
        solve_id: int | None = self.save_solve()

        if solve_id is None:
            raise ValueError("Failed to add solve to database.")
        else:
            self.query_one(StatsWidget).update(
                self.db.get_solve_ids_and_times_and_penalties(self.solve_buffer.session_id)
            )

        save_last_session_id(self.solve_buffer.session_id)

        # reset
        self.solve_buffer = SolveBuffer()
        self.solve_buffer.session_id = get_last_session_id()

    @on(ScrambleWidget.Changed)
    def update_cube_net(self, message: ScrambleWidget.Changed) -> None:
        try:
            self.cube_net_widget.update_cube_net(message.scramble, message.cube_size)

            self.solve_buffer.scramble = message.scramble
        except ValueError:
            self.notify("[#ff0000][b]Error[/][/]\nInvalid scramble", severity="error")
            self.query_one(ScrambleWidget).set_inputted_scramble(None)
