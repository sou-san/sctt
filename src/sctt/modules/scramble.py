import random
from typing import Literal

CUBE_SIZE_VARIANT = Literal[2, 3, 4, 5, 6, 7]


def _generate_2_layer_turn_moves(moves: list[str]) -> list[str]:
    """
    Args:
        moves: 任意の回転記号から、任意の 2 層回しをする回転記号を生成する。例 U -> Uw
    """

    return [move + "w" for move in moves]


def _generate_3_layer_turn_moves(moves: list[str]) -> list[str]:
    """
    Args:
        moves: 任意の 2 層回しの回転記号から、任意の 3 層回しをする回転記号を生成する。例 Uw -> 3Uw
    """

    return ["3" + move for move in moves if "w" in move]


def generate_scramble(cube_size: CUBE_SIZE_VARIANT = 3) -> str:
    """
    Args:
        cube_size: 例 3x3x3 -> 3 (デフォルト値)
    """

    moves: list[str] = ["L", "R", "U", "D", "F", "B"]
    # 方向(時計回り 90 度回転、反時計回り 90 度回転、180 度回転)
    # 180度回転 (U2 など) の確率を上げるために "2" を2つ設定
    modifiers: tuple[str, ...] = ("", "'", "2", "2")
    scramble_length: int

    match cube_size:
        case 2:
            scramble_length = 10
            moves.remove("L")
            moves.remove("D")
            moves.remove("B")
        case 3:
            scramble_length = 20
        case 4:
            scramble_length = 45
            moves.append("Uw")
            moves.append("Rw")
            moves.append("Fw")
        case 5:
            scramble_length = 60
            moves.extend(_generate_2_layer_turn_moves(moves))
        case 6:
            scramble_length = 80
            moves.extend(_generate_2_layer_turn_moves(moves))
            moves.extend(_generate_3_layer_turn_moves(moves))
        case 7:
            scramble_length = 100
            moves.extend(_generate_2_layer_turn_moves(moves))
            moves.extend(_generate_3_layer_turn_moves(moves))
        case _:
            raise ValueError(
                f"Invalid cube size: {cube_size}. Supported sizes are between 2 and 7."
            )

    previous: str = ""
    two_previous: str = ""
    scramble: list[str] = []

    for _ in range(scramble_length):
        move: str = random.choice(moves)

        # 同じ面の連続回転を避けるため、直前2つの回転と同じ動きは選ばない
        while move == previous or move == two_previous:
            move = random.choice(moves)

        two_previous = previous
        previous = move

        modifier: str = random.choice(modifiers)
        scramble.append(move + modifier)

    return " ".join(scramble)


# test
if __name__ == "__main__":
    print(f"Scramble: {generate_scramble(3)}")
