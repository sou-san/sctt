from sctt.modules.simulate import Cube


def test_apply_scramble() -> None:
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

    assert cube.faces == expected_faces
