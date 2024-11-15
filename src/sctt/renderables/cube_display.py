import os
from enum import Enum, auto
from typing import Generator

from rich.columns import Columns
from rich.console import group
from rich.text import Text

from sctt.modules.simulate import Cube

# x11 で Tmux を起動していると、tty で新たに起動した Tmux で正しく表示されなかった。
# tty で使う時は、 x11 の Tmux セッションをすべて終了させて、新たに tty で Tmux を起動する必要があるみたい。


class StickerSize(Enum):
    MINI = auto()
    NORMAL = auto()


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

    def __init__(self, cube: Cube, sticker_size: StickerSize = StickerSize.NORMAL) -> None:
        self.cube: Cube = cube
        self.sticker_size: StickerSize = sticker_size
        self.cube_net: list[list[list[Text]]] = []

    def _create_colored_sticker(self, color: str) -> Text:
        match self.sticker_size:
            case StickerSize.MINI:
                return Text("■", style=color)
            case StickerSize.NORMAL:
                # スタイルのために微調整
                return Text("██" + " \n", style=color)

    def _create_colored_face(self, face: list[list[str]]) -> list[list[Text]]:
        return [
            [self._create_colored_sticker(self.COLORS[color]) for color in row] for row in face
        ]

    def _set_colored_cube_net(self, faces: dict[str, list[list[str]]]) -> None:
        self.cube_net = [self._create_colored_face(face) for face in faces.values()]

    @group()
    def generate_renderable_cube_net(self) -> Generator[Columns, None, None]:
        self._set_colored_cube_net(self.cube.faces)

        space: list[Text] = [
            Text(" " * self._sticker_width) for _ in range(self.cube.size)
        ] + [Text(" ")]

        for i in range(self.cube.size):
            yield Columns(space + self.cube_net[0][i])

        yield Columns(" ")

        for i in range(self.cube.size):
            result: list[Text] = []

            for face in self.cube_net[1:5]:
                for line in face[i]:
                    result.append(line)

                result.append(Text(" "))

            yield Columns(result)

        yield Columns(" ")

        for i in range(self.cube.size):
            if i == self.cube.size - 1:
                tmp: list[Text] = []

                for rich_text in self.cube_net[-1][i]:
                    striped = self.strip_rich_text(rich_text, "\n")
                    tmp.append(striped)

                yield Columns(space + tmp)
            else:
                yield Columns(space + self.cube_net[-1][i])

    @staticmethod
    def strip_rich_text(rich_text: Text, chars: str | None = None) -> Text:
        """Text オブジェクトをスタイルを保持したまま strip() する"""

        return Text(rich_text.plain.strip(chars), style=rich_text.style)

    @property
    def _sticker_width(self) -> int:
        match self.sticker_size:
            case StickerSize.MINI:
                return 1
            case StickerSize.NORMAL:
                return 3

    @property
    def renderable_width(self) -> int:
        raw_width: int = self._sticker_width * self.cube.size * 4
        spaced_width: int = raw_width + (self.cube.size - 1) * 4

        match self.sticker_size:
            case StickerSize.MINI:
                return spaced_width + 3 * 3
            case StickerSize.NORMAL:
                return spaced_width + 3 * 3 - 1

    @property
    def renderable_height(self) -> int:
        match self.sticker_size:
            case StickerSize.MINI:
                return self.cube.size * 3 + 2
            case StickerSize.NORMAL:
                return self.cube.size * 3 + (self.cube.size - 1) * 3 + 2 * 2 + 1


# test
if __name__ == "__main__":
    from rich.console import Console

    from sctt.modules.simulate import Cube

    # 3x3x3 scramble
    scramble: str = "R' F2 U2 L2 F2 D2 B U2 B R2 F R2 D F L D2 U' R B R"
    # 7x7x7 scramble
    # scramble: str = "3Rw2 D 3Lw Uw2 Bw2 Uw' Lw' D' Dw' 3Lw' F B Rw' 3Uw 3Rw' 3Lw2 3Fw2 Rw' Lw 3Lw 3Bw Bw2 L 3Bw Fw2 Uw' 3Dw' 3Fw2 R D' 3Bw2 3Lw2 3Rw2 L2 3Uw R2 Rw 3Uw2 Lw' Bw Fw' 3Dw2 3Uw R' 3Lw2 L' B' Dw2 U' 3Dw Lw2 B 3Uw Bw' L' Dw' 3Uw' Bw2 Rw' Fw B' 3Lw' Bw' 3Dw2 Lw Uw Rw2 3Rw2 Fw2 Uw 3Dw' Bw' 3Uw Lw2 3Lw' 3Fw Dw' B 3Bw' R B 3Dw2 3Fw Uw' R2 L2 Lw' 3Lw2 Bw2 3Uw Fw' F2 Rw2 U2 3Rw2 D' 3Rw R' Lw2 3Bw'"

    console: Console = Console()
    cube: Cube = Cube(3)
    cube_display: CubeDisplay = CubeDisplay(cube, StickerSize.MINI)

    console.print(f"Scramble: {scramble}")
    console.print()
    console.print(cube_display.generate_renderable_cube_net())

    moves: list[str] = []

    for move in scramble.split(" "):
        moves.append(move)
        console.print("=" * 80)
        console.print("Moves:")
        console.print(" ".join(moves))
        console.print()

        cube.apply_scramble(move)

        console.print(cube_display.generate_renderable_cube_net())

    console.print(f"{cube_display.renderable_width} x {cube_display.renderable_height}")
