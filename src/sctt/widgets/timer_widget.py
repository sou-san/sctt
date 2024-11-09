from pathlib import Path

import keyboard
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static
from textual_pyfiglet.pyfiglet import figlet_format

from sctt.modules.timer import Timer, TimerState


class TimerWidget(Static):
    class Solved(Message):
        def __init__(self, time: str) -> None:
            super().__init__()
            self.time: str = time

    time: reactive[str] = reactive("")

    def __init__(self) -> None:
        super().__init__()
        self.font: Path = Path(__file__).parents[1] / "fonts" / "mono_banner"
        self.timer = Timer()

    def on_mount(self) -> None:
        keyboard.hook(self.key_events)
        self.set_interval(1 / 60, self.set_time)

    def set_time(self) -> None:
        self.time = figlet_format(
            self.timer.format_time().strip(), font=str(self.font), width=self.size.width
        ).strip("\n")

    def key_events(self, event: keyboard.KeyboardEvent) -> None:
        if isinstance(self.app.screen, ModalScreen) or event.name != "space":
            return

        match event.event_type:
            case keyboard.KEY_DOWN:
                if self.timer.state == TimerState.RUNNING:
                    self.post_message(self.Solved(self.time))

                self.timer.on_press()
            case keyboard.KEY_UP:
                self.timer.on_release()

        match self.timer.state:
            case TimerState.STOPPED:
                self.styles.color = "#fff 85%"
            case TimerState.WAITING_FOR_START:
                self.styles.color = "#f00 90%"
            case TimerState.READY_TO_START:
                self.styles.color = "#0f0 80%"
            case TimerState.RUNNING:
                self.styles.color = "#fff 85%"

        self.set_time()

    def watch_time(self, time: str) -> None:
        self.update(time)
