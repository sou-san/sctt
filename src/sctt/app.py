import keyboard
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.events import Resize
from textual.reactive import reactive
from textual.widgets import Footer

from sctt.modules.scramble import generate_scramble
from sctt.screens.blocking_screen import MIN_HEIGHT, MIN_WIDTH, BlockingScreen
from sctt.widgets.cube_net_widget import CubeNetWidget
from sctt.widgets.scramble_widget import ScrambleWidget

# from sctt.widgets.status_widget import StatusWidgets
from sctt.widgets.timer_widget import TimerWidget


class Sctt(App[None]):
    CSS_PATH = "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "", "Start / Stop"),  # Dummy key binding for the keyboard lib.
    ]

    scramble: reactive[str] = reactive(generate_scramble, init=False)

    def compose(self) -> ComposeResult:
        # with Horizontal():
        # バックエンドの処理などがまだできていないため、コメントアウトしている。
        # yield StatusWidgets()
        with VerticalScroll():
            with VerticalScroll():
                yield ScrambleWidget(self.scramble)
            self.timer_widget = TimerWidget()
            yield self.timer_widget
            yield CubeNetWidget(self.scramble)
        yield Footer()

    def watch_scramble(self, scramble: str) -> None:
        self.query_one(ScrambleWidget).update(scramble)
        self.query_one(CubeNetWidget).scramble = scramble

    def update_scramble(self) -> None:
        self.scramble = generate_scramble()

    def on_timer_widget_solved(self) -> None:
        self.update_scramble()

    def on_app_focus(self) -> None:
        keyboard.hook(self.timer_widget.key_events)

    def on_app_blur(self) -> None:
        keyboard.unhook_all()

    def on_resize(self, event: Resize) -> None:
        if event.size.width < MIN_WIDTH or event.size.height < MIN_HEIGHT:
            self.push_screen(BlockingScreen())
