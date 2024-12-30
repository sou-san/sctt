from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class DialogScreen(ModalScreen[str]):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text: str = text

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label(self.text)
            with Center():
                with Horizontal():
                    yield Button("Ok", id="ok")
                    yield Button("Cancel", id="cancel")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "cancel":
                self.dismiss("cancel")
            case "ok":
                self.dismiss("ok")
            case _:
                pass
