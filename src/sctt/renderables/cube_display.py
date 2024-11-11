import os
from typing import Generator, Literal

from rich.columns import Columns
from rich.console import group
from rich.text import Text

from sctt.modules.simulate import Cube

# x11 で Tmux を起動していると、tty で新たに起動した Tmux で正しく表示されなかった。
# tty で使う時は、 x11 の Tmux セッションをすべて終了させて、新たに tty で Tmux を起動する必要があるみたい。

STICKER_STYLE_VARIANT = Literal["mini filled", "filled"]


class CubeDisplay:
    IS_TTY: bool = os.getenv("XDG_SESSION_TYPE") == "tty"

    COLORS: dict[str, str] = {
        "W": "#dddddd",  # 眩しさを軽減
        # Linux console (tty) 環境では表示できる色が限られているのでマゼンタ色にする。
        "O": "#ff00ff" if IS_TTY else "#ff8f00",  # Magenta or Orange
        "G": "#00cc00",  # 眩しさを軽減
        "R": "#ee0000",  # ff0000 にすると、何故か vscode で表示が崩れるから代わりに ee0000 を指定する。
        "B": "#0055ff",  # 0000ff にすると、 vscode で見づらいから 0055ff を指定する。
        "Y": "#ffee00",  # 眩しさを軽減
    }

    def __init__(self, cube: Cube, sticker_style: STICKER_STYLE_VARIANT = "filled") -> None:
        self.cube: Cube = cube
        self.sticker_style: str = sticker_style
        self.cube_net: list[list[list[Text]]] = []

    def _create_colored_sticker(self, color: str) -> Text:
        if self.sticker_style == "mini filled":
            return Text("■", style=color)

        # スタイルのために微調整
        return Text("██" + " \n", style=color)

    def _create_colored_face(self, face: list[list[str]]) -> list[list[Text]]:
        return [[self._create_colored_sticker(self.COLORS[color]) for color in row] for row in face]

    def _set_colored_cube_net(self, faces: dict[str, list[list[str]]]) -> None:
        self.cube_net = [self._create_colored_face(face) for face in faces.values()]

    @group()
    def generate_renderable_cube_net(self) -> Generator[Columns, None, None]:
        self._set_colored_cube_net(self.cube.faces)

        space: list[Text] = [Text(" ") for _ in range(self._sticker_width * self.cube.size)]

        for i in range(self.cube.size):
            yield Columns(space + self.cube_net[0][i])

        for i in range(self.cube.size):
            yield Columns([line for face in self.cube_net[1:5] for line in face[i]])

        for i in range(self.cube.size):
            yield Columns(space + self.cube_net[-1][i])

    @property
    def _sticker_width(self) -> int:
        return 1 if self.sticker_style == "mini filled" else 2

    @property
    def renderable_width(self) -> int:
        assert self.sticker_style in ("mini filled", "filled")

        match self.sticker_style:
            case "mini filled":
                return self.cube.size * self._sticker_width * 4
            case "filled":
                return self.cube.size * self._sticker_width * 4 * 2

    @property
    def renderable_height(self) -> int:
        assert self.sticker_style in ("mini filled", "filled")

        match self.sticker_style:
            case "mini filled":
                return self.cube.size * 3
            case "filled":
                return self.cube.size * 3 * 2


# test
if __name__ == "__main__":
    from rich.console import Console

    from sctt.modules.simulate import Cube

    scramble: str = "R' F2 U2 L2 F2 D2 B U2 B R2 F R2 D F L D2 U' R B R"

    console: Console = Console()
    cube: Cube = Cube()
    cube_display: CubeDisplay = CubeDisplay(cube, "filled")

    console.print(f"Scramble: {scramble}", end="\n\n")

    console.print(cube_display.generate_renderable_cube_net())
    console.print("=" * 60, end="\n\n")
    cube.apply_scramble(scramble)
    console.print(cube_display.generate_renderable_cube_net())

    console.print(f"{cube_display.renderable_width} x {cube_display.renderable_height}")
