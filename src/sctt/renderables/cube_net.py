import os
from enum import Enum, auto
from itertools import chain

from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style

from sctt.modules.simulate import Cube

# x11 で Tmux を起動しているとき tty で新たに起動した Tmux で CubeNet の色が正しく表示されなかった。
# XDG_SESSION_TYPE の値が x11 から tty に変わらないみたい。
# tty で使うときは x11 の Tmux セッションをすべて終了させて、 tty で新たに Tmux を起動する必要があるみたい。
# (Tmux 3.4)


class StickerSize(Enum):
    MINI = auto()
    NORMAL = auto()


class CubeNet:
    IS_TTY: bool = os.getenv("XDG_SESSION_TYPE") == "tty"
    COLOR_MAP: dict[str, str] = {
        "W": "#dddddd",  # 眩しさを軽減
        # Linux console (tty) 環境では表示できる色が限られているのでマゼンタ色にする。
        "O": "#ff00ff" if IS_TTY else "#ff8f00",  # Magenta or Orange
        "G": "#00cc00",  # 眩しさを軽減
        "R": "#ee0000",  # ff0000 にすると、何故か vscode で表示が崩れるから代わりに ee0000 を指定する。
        "B": "#0055ff",  # 0000ff にすると、 vscode で見づらいから 0055ff を指定する。
        "Y": "#ffee00",  # 眩しさを軽減
    }

    def __init__(self, size: int = 3, sticker_size: StickerSize = StickerSize.NORMAL) -> None:
        self._cube: Cube = Cube(size)
        self.sticker_size = sticker_size

    def _set_sticker_values(self, sticker_size: StickerSize) -> None:
        self._sticker_size: StickerSize = sticker_size

        self._sticker: str
        self._letter_spacing: int
        self._line_spacing: int
        self._face_right_padding: int
        self._face_bottom_padding: int

        match sticker_size:
            case StickerSize.MINI:
                self._sticker = "■"
                self._letter_spacing = 1
                self._line_spacing = 0
                self._face_right_padding = 3
                self._face_bottom_padding = 1
            case StickerSize.NORMAL:
                self._sticker = "██"
                self._letter_spacing = 2
                self._line_spacing = 1
                self._face_right_padding = 4
                self._face_bottom_padding = 2

    @property
    def size(self) -> int:
        return self._cube.size

    @property
    def sticker_size(self) -> StickerSize:
        return self._sticker_size

    @sticker_size.setter
    def sticker_size(self, sticker_size: StickerSize) -> None:
        self._set_sticker_values(sticker_size)

    @property
    def _sticker_width(self) -> int:
        return len(self._sticker)

    @property
    def width(self) -> int:
        return (
            self._sticker_width * self._cube.size * 4
            + self._letter_spacing * (self._cube.size - 1) * 4
            + self._face_right_padding * 3
        )

    @property
    def height(self) -> int:
        return (
            self._cube.size * 3
            + self._line_spacing * (self._cube.size - 1) * 3
            + self._face_bottom_padding * 2
        )

    def _create_sticker(self, sticker: str, color_char: str | None = None) -> RenderResult:
        style = Style(color=self.COLOR_MAP[color_char]) if color_char is not None else None
        yield Segment(sticker, style=style)

    def _create_dummy_face_row(self) -> RenderResult:
        for i in range(1, self._cube.size + 1):
            # デバック時にスペースでは見にくいので色付きのダミーステッカーを使う。
            # yield Segment(self._sticker, Style(color="#252525"))
            yield from self._create_sticker(" " * self._sticker_width)

            if i < self._cube.size:
                yield Segment(" " * self._letter_spacing)

    def _render_top_face(self) -> RenderResult:
        for i, face_row in enumerate(self._cube.faces["U"], start=1):
            # Prefix
            yield from self._create_dummy_face_row()
            yield Segment(" " * self._face_right_padding)

            for j, color_char in enumerate(face_row, start=1):
                yield from self._create_sticker(self._sticker, color_char)

                if j < self._cube.size:
                    yield Segment(" " * self._letter_spacing)

            yield Segment("\n")

            if i < self._cube.size:
                yield Segment("\n" * self._line_spacing)

    def _render_middle_faces(self) -> RenderResult:
        zipped = zip(
            self._cube.faces["L"],
            self._cube.faces["F"],
            self._cube.faces["R"],
            self._cube.faces["B"],
            strict=False,
        )

        for i, faces_rows in enumerate(zipped, start=1):
            for j, color_char in enumerate(chain.from_iterable(faces_rows)):
                yield from self._create_sticker(self._sticker, color_char)

                if j % self._cube.size == self._cube.size - 1:
                    yield Segment(" " * self._face_right_padding)
                else:
                    yield Segment(" " * self._letter_spacing)

            yield Segment("\n")

            if i < self._cube.size:
                yield Segment("\n" * self._line_spacing)

    def _render_bottom_face(self) -> RenderResult:
        for i, face_row in enumerate(self._cube.faces["D"], start=1):
            # Prefix
            yield from self._create_dummy_face_row()
            yield Segment(" " * self._face_right_padding)

            for j, color_char in enumerate(face_row, start=1):
                yield from self._create_sticker(self._sticker, color_char)

                if j < self._cube.size:
                    yield Segment(" " * self._letter_spacing)

            yield Segment("\n")

            if i < self._cube.size:
                yield Segment("\n" * self._line_spacing)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield from self._render_top_face()
        yield Segment("\n" * self._face_bottom_padding)
        yield from self._render_middle_faces()
        yield Segment("\n" * self._face_bottom_padding)
        yield from self._render_bottom_face()

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement(self.width, self.width)

    def initialize(self) -> None:
        self._cube.initialize()

    def apply_scramble(self, scramble: str) -> None:
        self._cube.apply_scramble(scramble)


# demo
if __name__ == "__main__":
    from rich.console import Console

    SCRAMBLES: dict[int, str] = {
        2: "F R2 F2 R2 U R F2 R2 U2",
        3: "F U' L2 B2 U' R2 B2 R2 D' L2 U L2 U R F L D' R' F R F2",
        4: "D2 L2 F U2 R2 D2 R2 B U2 B' U2 F2 D F2 B U2 R U2 R B' L Fw2 Uw2 L2 U' F2 Fw2 D R2 L' Fw2 L2 U Uw2 Fw D' Fw2 L U L Uw L' F' R' Rw' Uw2 Rw",
        5: "Rw Uw' Rw' L Dw Bw' B U' F' Dw' Rw2 D' Bw' Dw' Uw2 U Lw' Rw2 R2 U D' Lw2 Bw Rw U Rw' F Bw Lw Uw' Dw Bw Lw' R2 U' Lw2 Dw L' F U L Bw2 U2 Fw2 Uw2 B2 R' U Fw F2 Lw2 U' F Lw' D' F' Rw' F Bw' R2",
        6: "3Fw2 R2 L Bw' F' Fw' Dw Lw2 B' Uw2 R2 Lw2 Dw' Fw' 3Fw2 Lw' Uw' 3Uw2 3Rw' Uw' U' B 3Rw R' B 3Fw2 3Uw' Dw' 3Rw Bw2 Uw2 Lw Rw 3Uw2 L' B Lw 3Rw2 B2 F 3Fw2 Bw' Rw2 B2 Uw 3Rw2 F2 3Rw' U' 3Rw Bw' L U F Lw L F2 3Rw' Uw2 Fw2 3Fw2 R2 Dw' 3Uw 3Rw' Lw2 Rw U D' Fw R' D 3Uw' Dw2 L Uw D2 R Uw' Dw2",
        7: "3Rw2 3Dw Uw 3Bw' L' U Rw 3Lw U2 Lw2 3Rw2 3Fw L 3Dw 3Uw 3Fw' R' D 3Fw L2 Rw Fw2 Bw2 B R2 3Bw' 3Rw2 3Dw' Lw U' Fw' 3Uw' 3Fw2 R 3Bw Rw 3Rw2 Fw2 F' Bw L Rw2 Fw U' Rw' 3Lw' 3Bw' F D' Bw2 Dw' R B2 F2 U2 Bw 3Bw Lw Fw' 3Bw 3Rw' F 3Bw 3Rw2 B 3Dw F L Fw2 D2 R' 3Dw2 L2 3Fw Rw2 Bw2 3Lw Rw' B' Uw2 F' 3Rw2 F2 3Fw B 3Rw2 3Uw' Bw' R' 3Bw' Uw' Bw' 3Dw' 3Lw2 Dw2 Uw2 3Uw2 F2 U' Lw'",
    }
    console: Console = Console()

    for sticker_size in StickerSize:
        for size, scramble in SCRAMBLES.items():
            cube_net: CubeNet = CubeNet(size=size, sticker_size=sticker_size)
            cube_net.apply_scramble(scramble)

            console.print("=" * 80)
            console.print(f"Scramble: {scramble}")
            console.print()
            console.print(cube_net)
