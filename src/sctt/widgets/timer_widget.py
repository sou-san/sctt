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

    time: reactive[str] = reactive("")

    def __init__(self) -> None:
        super().__init__()
        self.font: Path = Path(__file__).parents[1] / "fonts" / "mono_banner"
        self.timer = Timer()

    def on_mount(self) -> None:
        try:
            keyboard.hook(self.key_events)
        except ImportError:
            self.app.exit(
                return_code=13,
                message="You must be root to use sctt on linux.\n\nsudo -E $(which sctt)",
            )
        else:
            self.set_interval(1 / 60, self.set_time)

    def style_time(self) -> str:
        formatted_time: str = self.timer.format_time(
            self.timer.get_elapsed_time(), timer_state=True
        )
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

    def key_events(self, event: keyboard.KeyboardEvent) -> None:
        if isinstance(self.app.screen, ModalScreen) or event.name != "space":
            return

        match event.event_type:
            case keyboard.KEY_DOWN:
                if self.timer.state == TimerState.RUNNING:
                    self.post_message(self.Solved(self.timer.get_elapsed_time()))

                self.timer.on_press()
            case keyboard.KEY_UP:
                self.timer.on_release()
            case _:
                pass

        match self.timer.state:
            case TimerState.STOPPED:
                self.styles.color = "#fff 85%"
            case TimerState.WAITING_FOR_START:
                self.styles.color = "#f00 90%"
            case TimerState.READY_TO_START:
                self.styles.color = "#0f0 80%"
            case TimerState.RUNNING:
                self.styles.color = "#fff 85%"
