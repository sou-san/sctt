from textual.app import ComposeResult
from textual.widgets import Static

from sctt.modules.simulate import Cube
from sctt.renderables.cube_display import CubeDisplay, StickerSize
from sctt.widgets.my_vertical_scroll import MyVerticalScroll


class CubeNetDisplay(Static):
    pass


class CubeNetWidget(MyVerticalScroll):
    def compose(self) -> ComposeResult:
        yield CubeNetDisplay()

    def update_cube_net(self, scramble: str, cube_size: int) -> None:
        match cube_size:
            case 2 | 3 | 4 | 5 | 6 | 7:
                cube = Cube(cube_size)
                cube.apply_scramble(scramble)
                cube_display = CubeDisplay(cube, StickerSize.NORMAL)

                if (
                    cube_display.renderable_width > self.size.width
                    or cube_display.renderable_height > self.size.height
                ):
                    cube_display = CubeDisplay(cube, StickerSize.MINI)

                cube_net = cube_display.generate_renderable_cube_net()
                self.query_one(CubeNetDisplay).update(cube_net)
            case _:
                pass
