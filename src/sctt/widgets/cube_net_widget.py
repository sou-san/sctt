from textual.app import ComposeResult
from textual.widgets import Static

from sctt.renderables.cube_net import CubeNet, StickerSize
from sctt.widgets.my_scrollable_container import MyScrollableContainer


class CubeNetDisplay(Static):
    pass


class CubeNetWidget(MyScrollableContainer):
    def compose(self) -> ComposeResult:
        yield CubeNetDisplay()

    def __init__(self, cube_size: int = 3) -> None:
        super().__init__()
        self._cube_net = CubeNet(cube_size)

    @property
    def cube_size(self) -> int:
        return self._cube_net.size

    @cube_size.setter
    def cube_size(self, cube_size: int) -> None:
        self._cube_net = CubeNet(cube_size)

    @property
    def can_focus(self) -> bool:
        return self.show_vertical_scrollbar or self.show_horizontal_scrollbar

    @can_focus.setter
    def can_focus(self, flag: bool) -> None:
        self.can_focus = flag

    def update(self) -> None:
        self._cube_net.sticker_size = StickerSize.NORMAL

        if self._cube_net.width > self.size.width or self._cube_net.height > self.size.height:
            self._cube_net.sticker_size = StickerSize.MINI

        self.query_one(CubeNetDisplay).update(self._cube_net)

    def initialize(self) -> None:
        self._cube_net.initialize()

    def apply_scramble(self, scramble: str) -> None:
        self._cube_net.apply_scramble(scramble)

    def on_resize(self) -> None:
        self.update()


# demo
if __name__ == "__main__":
    from textual import events
    from textual.app import App, ComposeResult

    from sctt.modules.scramble import generate_scramble

    class DemoCubeNetApp(App[None]):
        CSS = """
        * {
            scrollbar-size-vertical: 1;
            scrollbar-background: #000000;
            scrollbar-background-active: #000000;
            scrollbar-background-hover: #000000;
            scrollbar-color: #808080;
            scrollbar-color-active: #00ff00;
            scrollbar-color-hover: #aaaaaa;
        }

        Screen {
            align: center middle;
        }

        CubeNetWidget {
            align: center middle;
            width: 60%;
            height: 60%;
            border: round #00ff00;

            CubeNetDisplay {
                width: auto;
                height: auto;
            }
        }
        """

        def __init__(self) -> None:
            super().__init__()
            self.cube_size: int = 3
            self.scramble: str = generate_scramble(self.cube_size)

        def compose(self) -> ComposeResult:
            yield CubeNetWidget(self.cube_size)

        def on_mount(self) -> None:
            self.update_cube_net()

        def update_cube_net(self) -> None:
            cube_net: CubeNetWidget = self.query_one(CubeNetWidget)
            cube_net.initialize()
            cube_net.cube_size = self.cube_size
            cube_net.apply_scramble(self.scramble)
            cube_net.update()

        def initialize_cube_net(self) -> None:
            cube_net: CubeNetWidget = self.query_one(CubeNetWidget)
            cube_net.initialize()
            cube_net.update()

        def on_key(self, event: events.Key) -> None:
            if event.key == "escape":
                self.initialize_cube_net()

            try:
                if (n := int(event.key)) in range(2, 8):
                    self.cube_size = n
                    self.scramble = generate_scramble(n)
                    self.update_cube_net()
            except ValueError:
                pass

    DemoCubeNetApp().run()
