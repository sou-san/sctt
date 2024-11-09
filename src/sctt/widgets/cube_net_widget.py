from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget

from sctt.modules.simulate import Cube
from sctt.renderables.cube_display import CubeDisplay


class CubeNetWidget(Widget):
    scramble: reactive[str] = reactive("", init=False)

    def __init__(self, scramble: str) -> None:
        super().__init__()
        self.scramble = scramble

    def watch_scramble(self) -> None:
        cube = Cube()
        cube.apply_scramble(self.scramble)
        self.cube_net = CubeDisplay(cube, "filled").generate_renderable_cube_net()

    def render(self) -> RenderResult:
        return self.cube_net
