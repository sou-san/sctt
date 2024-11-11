import copy
from typing import Callable


class Cube:
    """ルービックキューブの状態をシュミレーションするクラス"""

    """
    例 3x3x3 キューブの展開図とナンバリング (リストのインデックス):
    W -> White
    O -> Orange
    G -> Green
    R -> Red
    B -> Blue
    Y -> Yellow

                       W  W  W                                                    0  1  2
                Up ->  W  W  W   __Front                                   Up ->  0  1  2   __Front
                       W  W  W  /     __ Right                                    0  1  2  /     __ Right
                               /     /                                                    /     /
             O  O  O   G  G  G   R  R  R   B  B  B                      0  1  2   0  1  2   0  1  2   0  1  2
    Left ->  O  O  O   G  G  G   R  R  R   B  B  B  <- Back    Left ->  0  1  2   0  1  2   0  1  2   0  1  2  <- Back
             O  O  O   G  G  G   R  R  R   B  B  B                      0  1  2   0  1  2   0  1  2   0  1  2

                       Y  Y  Y                                                    0  1  2
              Down ->  Y  Y  Y                                           Down ->  0  1  2
                       Y  Y  Y                                                    0  1  2

    U 面を白色、F 面を緑色で固定して操作を考える。
    """

    VALID_MOVES: set["str"] = {
        # 1層回し
        "U",
        "D",
        "L",
        "R",
        "F",
        "B",
        "U'",
        "D'",
        "L'",
        "R'",
        "F'",
        "B'",
        "U2",
        "D2",
        "L2",
        "R2",
        "F2",
        "B2",
        # 2層回し
        "Uw",
        "Dw",
        "Lw",
        "Rw",
        "Fw",
        "Bw",
        "Uw'",
        "Dw'",
        "Lw'",
        "Rw'",
        "Fw'",
        "Bw'",
        "Uw2",
        "Dw2",
        "Lw2",
        "Rw2",
        "Fw2",
        "Bw2",
        # 3層回し
        "3Uw",
        "3Dw",
        "3Lw",
        "3Rw",
        "3Fw",
        "3Bw",
        "3Uw'",
        "3Dw'",
        "3Lw'",
        "3Rw'",
        "3Fw'",
        "3Bw'",
        "3Uw2",
        "3Dw2",
        "3Lw2",
        "3Rw2",
        "3Fw2",
        "3Bw2",
    }

    def __init__(self, size: int = 3) -> None:
        """
        Args:
            size: example 3x3x3 -> 3 (現在は 3x3x3 (3) しか対応していない)
        """

        if self.is_natural_number(size):
            self.size: int = size
        else:
            raise ValueError("size must be a natural number")

        self.initialize()

    @staticmethod
    def is_natural_number(n: int) -> bool:
        return n > 0

    def initialize(self) -> None:
        self.faces: dict[str, list[list[str]]] = {
            "U": [["W"] * self.size for _ in range(self.size)],
            "L": [["O"] * self.size for _ in range(self.size)],
            "F": [["G"] * self.size for _ in range(self.size)],
            "R": [["R"] * self.size for _ in range(self.size)],
            "B": [["B"] * self.size for _ in range(self.size)],
            "D": [["Y"] * self.size for _ in range(self.size)],
        }

    def _rotate_face_clockwise(self, face: str) -> None:
        # 指定された面を時計回りに回転させる
        self.faces[face] = [
            list(row) for row in zip(*self.faces[face][::-1], strict=True)
        ]

    def _move_u(self) -> None:
        # U 面を時計回り回転
        self._rotate_face_clockwise("U")

        # U 面の側面一列を時計回りにシフト
        tmp: list[str] = self.faces["F"][0][:]
        self.faces["F"][0] = self.faces["R"][0][:]
        self.faces["R"][0] = self.faces["B"][0][:]
        self.faces["B"][0] = self.faces["L"][0][:]
        self.faces["L"][0] = tmp

    def _move_d(self) -> None:
        # D 面を時計回り回転
        self._rotate_face_clockwise("D")

        # D 面の側面一列を時計回りにシフト
        tmp: list[str] = self.faces["F"][self.size - 1][:]
        self.faces["F"][self.size - 1] = self.faces["L"][self.size - 1][:]
        self.faces["L"][self.size - 1] = self.faces["B"][self.size - 1][:]
        self.faces["B"][self.size - 1] = self.faces["R"][self.size - 1][:]
        self.faces["R"][self.size - 1] = tmp

    def _move_l(self) -> None:
        # L 面を時計回り回転
        self._rotate_face_clockwise("L")

        # L 面の側面一列を時計回りにシフト
        tmp: list[str] = [self.faces["U"][i][0] for i in range(self.size)]
        for i in range(self.size):
            self.faces["U"][i][0] = self.faces["B"][self.size - 1 - i][self.size - 1]
            self.faces["B"][self.size - 1 - i][self.size - 1] = self.faces["D"][i][0]
            self.faces["D"][i][0] = self.faces["F"][i][0]
            self.faces["F"][i][0] = tmp[i]

    def _move_r(self) -> None:
        # R 面を時計回り回転
        self._rotate_face_clockwise("R")

        # R 面の側面一列を時計回りにシフト
        tmp: list[str] = [self.faces["U"][i][self.size - 1] for i in range(self.size)]
        for i in range(self.size):
            self.faces["U"][i][self.size - 1] = self.faces["F"][i][self.size - 1]
            self.faces["F"][i][self.size - 1] = self.faces["D"][i][self.size - 1]
            self.faces["D"][i][self.size - 1] = self.faces["B"][self.size - 1 - i][0]
            self.faces["B"][self.size - 1 - i][0] = tmp[i]

    def _move_f(self) -> None:
        # F 面を時計回りに回転
        self._rotate_face_clockwise("F")

        new_u: list[list[str]] = copy.deepcopy(self.faces["U"])
        new_l: list[list[str]] = copy.deepcopy(self.faces["L"])
        new_d: list[list[str]] = copy.deepcopy(self.faces["D"])
        new_r: list[list[str]] = copy.deepcopy(self.faces["R"])

        # F 面の側面一列を時計回りにシフト
        for i in range(self.size):
            # U 面の最下行 -> L 面の最右列（逆順）
            new_u[self.size - 1][i] = self.faces["L"][self.size - 1 - i][self.size - 1]
            # L 面の最右列 -> D 面の最上行
            new_l[i][self.size - 1] = self.faces["D"][0][i]
            # D 面の最上行 -> R 面の最左列（逆順）
            new_d[0][i] = self.faces["R"][self.size - 1 - i][0]
            # R 面の最左列 -> U 面の最下行
            new_r[i][0] = self.faces["U"][self.size - 1][i]

        self.faces["U"], self.faces["L"], self.faces["D"], self.faces["R"] = (
            new_u,
            new_l,
            new_d,
            new_r,
        )

    def _move_b(self) -> None:
        # B 面を時計回りに回転
        self._rotate_face_clockwise("B")

        new_u: list[list[str]] = copy.deepcopy(self.faces["U"])
        new_r: list[list[str]] = copy.deepcopy(self.faces["R"])
        new_d: list[list[str]] = copy.deepcopy(self.faces["D"])
        new_l: list[list[str]] = copy.deepcopy(self.faces["L"])

        # B 面の側面一列を時計回りにシフト
        for i in range(self.size):
            # U 面の最上行 -> R 面の最右列
            new_u[0][i] = self.faces["R"][i][self.size - 1]
            # R 面の最右列 -> D 面の最下行(逆順)
            new_r[i][self.size - 1] = self.faces["D"][self.size - 1][self.size - 1 - i]
            # D 面の最下行 -> L 面の最右列
            new_d[self.size - 1][i] = self.faces["L"][i][0]
            # L 面の最右列 -> U 面の最上行(逆順)
            new_l[i][0] = self.faces["U"][0][self.size - 1 - i]

        self.faces["U"], self.faces["R"], self.faces["D"], self.faces["L"] = (
            new_u,
            new_r,
            new_d,
            new_l,
        )

    def _get_num_moves(self, move: str) -> int:
        if "2" in move:
            return 2
        elif "'" in move:
            return 3
        else:
            return 1

    def apply_scramble(self, scramble: str) -> None:
        moves_map: dict[str, Callable[[], None]] = {
            "U": self._move_u,
            "D": self._move_d,
            "L": self._move_l,
            "R": self._move_r,
            "F": self._move_f,
            "B": self._move_b,
        }

        for move in scramble.split(" "):
            if move not in self.VALID_MOVES:
                raise ValueError(f"{scramble} is invalid scramble.")

            num_moves: int = self._get_num_moves(move)

            for _ in range(num_moves):
                moves_map[move[0]]()

        # TODO: Uw や 3Uw などの多層回しの適用を実装する。


# test
if __name__ == "__main__":
    scramble: str = "R' F2 U2 L2 F2 D2 B U2 B R2 F R2 D F L D2 U' R B R"
    expected_faces: dict[str, list[list[str]]] = {
        "U": [["O", "B", "Y"], ["W", "W", "R"], ["O", "G", "Y"]],
        "L": [["W", "B", "W"], ["Y", "O", "O"], ["R", "W", "Y"]],
        "F": [["B", "W", "G"], ["W", "G", "Y"], ["R", "R", "R"]],
        "R": [["O", "G", "O"], ["R", "R", "O"], ["G", "O", "R"]],
        "B": [["B", "Y", "G"], ["G", "B", "O"], ["Y", "Y", "B"]],
        "D": [["B", "B", "W"], ["R", "Y", "B"], ["W", "G", "G"]],
    }

    cube: Cube = Cube()
    cube.apply_scramble(scramble)

    assert cube.faces == expected_faces, "Test failed. Faces do not match expected state."
    print("Passed the test.")
