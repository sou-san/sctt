import keyboard
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.events import Resize
from textual.widgets import Footer

from sctt.screens.blocking_screen import MIN_HEIGHT, MIN_WIDTH, BlockingScreen
from sctt.widgets.cube_net_widget import CubeNetWidget
from sctt.widgets.scramble_widget import ScrambleWidget

# from sctt.widgets.status_widget import StatusWidgets
from sctt.widgets.timer_widget import TimerWidget


class AppBody(Vertical):
    pass


class Sctt(App[None]):
    CSS_PATH = "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "", "Start / Stop"),  # Dummy key binding for the keyboard lib.
    ]

    def compose(self) -> ComposeResult:
        # with Horizontal():
        # バックエンドの処理などがまだできていないため、コメントアウトしている。
        # yield StatusWidgets()
        with AppBody():
            yield ScrambleWidget()
            self.timer_widget = TimerWidget()
            yield self.timer_widget
            yield CubeNetWidget()
            yield Footer()

    def on_app_focus(self) -> None:
        keyboard.hook(self.timer_widget.key_events)

    def on_app_blur(self) -> None:
        keyboard.unhook_all()

    def on_resize(self, event: Resize) -> None:
        if event.size.width < MIN_WIDTH or event.size.height < MIN_HEIGHT:
            self.push_screen(BlockingScreen())

    @on(TimerWidget.Solved)
    def update_scramble(self) -> None:
        self.query_one(ScrambleWidget).update_scramble()

    @on(ScrambleWidget.Changed)
    async def update_cube_net(self, message: ScrambleWidget.Changed) -> None:
        self.query_one(CubeNetWidget).update_cube_net(message.scramble, message.cube_size)
