from pathlib import Path

import keyboard
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static
from textual_pyfiglet.pyfiglet import CharNotPrinted, figlet_format

from sctt.modules.timer import Timer, TimerState


class TimerWidget(Static):
    class Solved(Message):
        def __init__(self, time: float) -> None:
            super().__init__()
            self.time_: float = time

    STATE_CLASSES: dict[TimerState, str] = {
        TimerState.STOPPED: "stopped",
        TimerState.WAITING_FOR_START: "waiting-for-start",
        TimerState.READY_TO_START: "ready-to-start",
        TimerState.RUNNING: "running",
    }

    time: reactive[str] = reactive("")

    def __init__(self) -> None:
        super().__init__()
        self.font: Path = Path(__file__).parents[1] / "fonts" / "mono_banner"
        self.timer: Timer = Timer()

    def on_mount(self) -> None:
        try:
            keyboard.hook(self._handle_key_events)
        except ImportError:
            self.app.exit(
                return_code=13,
                message="You must be root to use sctt on linux.\n\nsudo -E $(which sctt)",
            )
        except AssertionError:
            self.app.exit(
                return_code=1,
                message="Sctt dose not support this environment.",
            )
        else:
            self.set_interval(1 / 60, self.set_time)

    def reset(self) -> None:
        self.timer.reset()

    def style_time(self) -> str:
        decimal_places: int

        match self.timer.state:
            case TimerState.RUNNING:
                decimal_places = 1
            case _:
                decimal_places = 2

        formatted_time: str = Timer.format_time(self.timer.elapsed_time, decimal_places)
        styled_time: str = str(
            figlet_format(formatted_time, str(self.font), width=self.size.width)
        )
        return styled_time.strip("\n")

    def set_time(self) -> None:
        try:
            self.time = self.style_time()
        except CharNotPrinted:
            # 起動時に self.size.width の値が 0 になる場合にアプリが落ちるのを防ぐ。
            pass

    def watch_time(self, time: str) -> None:
        self.update(time)

    def _update_state_color(self) -> None:
        self.set_classes(self.STATE_CLASSES[self.timer.state])

    def _handle_key_events(self, event: keyboard.KeyboardEvent) -> None:
        if (
            isinstance(self.app.screen, ModalScreen)
            or event.event_type is None
            or event.name != "space"
        ):
            return

        match event.event_type:
            case keyboard.KEY_DOWN:
                if self.timer.state == TimerState.RUNNING:
                    self.post_message(self.Solved(self.timer.elapsed_time))

                self.timer.on_press()
            case keyboard.KEY_UP:
                self.timer.on_release()

        self._update_state_color()

    def on_app_focus(self) -> None:
        keyboard.hook(self._handle_key_events)

    def on_app_blur(self) -> None:
        keyboard.unhook_all()
