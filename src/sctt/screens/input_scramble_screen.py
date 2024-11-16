from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea


class InputScrambleScreen(ModalScreen[str | None]):
    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Label("Input scramble")
            yield TextArea()
            with Horizontal():
                yield Button("Ok", id="ok")
                yield Button("Cancel", id="cancel")

    @on(Button.Pressed, "#ok")
    def get_inputted_scrambles(self) -> None:
        scramble: str = self.query_one(TextArea).text
        self.dismiss(scramble)

    @on(Button.Pressed, "#cancel")
    def close_screen(self) -> None:
        self.dismiss()
