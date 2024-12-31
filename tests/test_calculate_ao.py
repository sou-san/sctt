import math

from sctt.modules.calculate_ao import calculate_ao, my_round


def test_my_round() -> None:
    assert my_round(12.783, 2) == 12.78
    assert my_round(13.865, 2) == 13.87
    assert my_round(35.0493072839, 5) == 35.04931


def test_calculate_ao_no_solves() -> None:
    result: float | str = calculate_ao([], 5)

    if isinstance(result, float):
        assert math.isnan(result)
    else:
        raise


def test_calculate_ao_5() -> None:
    solves: list[tuple[float, str]]

    solves = [(15.91, ""), (16.71, ""), (10.31, ""), (19.38, ""), (19.51, "")]
    assert calculate_ao(solves, 5) == 17.333333333333332

    solves = [(15.91, "plus_2"), (16.71, ""), (10.31, "plus_2"), (19.38, ""), (19.51, "")]
    assert calculate_ao(solves, 5) == 18.0

    solves = [(15.91, "dnf"), (16.71, ""), (10.31, "dnf"), (19.38, ""), (19.51, "")]
    assert calculate_ao(solves, 5) == "DNF"


def test_calculate_ao_12() -> None:
    solves: list[tuple[float, str]]

    solves = [
        (15.91, ""),
        (16.71, ""),
        (10.31, ""),  #
        (19.38, ""),
        (19.51, ""),  #
        (14.22, ""),
        (13.85, ""),
        (12.43, ""),
        (17.65, ""),
        (18.14, ""),
        (16.01, ""),
        (11.34, ""),
    ]
    assert calculate_ao(solves, 12) == 15.563999999999998

    solves = [
        (15.91, "plus_2"),
        (16.71, "plus_2"),
        (10.31, "plus_2"),  #
        (19.38, "plus_2"),  #
        (19.51, ""),
        (14.22, ""),
        (13.85, ""),
        (12.43, ""),
        (17.65, "plus_2"),
        (18.14, ""),
        (16.01, ""),
        (11.34, "plus_2"),
    ]
    assert calculate_ao(solves, 12) == 16.377000000000002

    solves = [
        (15.91, ""),
        (16.71, ""),
        (10.31, ""),
        (19.38, ""),
        (19.51, ""),
        (14.22, "dnf"),
        (13.85, ""),
        (12.43, ""),
        (17.65, ""),
        (18.14, ""),
        (16.01, ""),
        (11.34, "dnf"),
    ]
    assert calculate_ao(solves, 12) == "DNF"


def test_calculate_ao_100() -> None:
    solves: list[tuple[float, str]]

    solves = [
        (11.51, ""),
        (14.47, ""),
        (14.05, ""),
        (13.74, ""),
        (14.65, ""),
        (14.47, ""),
        (16.40, ""),
        (13.53, ""),
        (13.64, ""),
        (15.30, ""),
        (13.14, ""),
        (14.07, ""),
        (14.52, ""),
        (11.84, ""),
        (12.12, ""),
        (15.64, ""),
        (15.72, ""),
        (13.34, ""),
        (16.80, ""),
        (17.10, ""),
        (13.97, ""),
        (16.04, ""),
        (12.03, ""),
        (15.69, ""),
        (15.56, ""),
        (10.97, ""),
        (11.40, ""),
        (16.17, ""),
        (13.29, ""),
        (14.18, ""),
        (11.49, ""),
        (15.49, ""),
        (14.99, ""),
        (13.95, ""),
        (16.82, ""),
        (15.47, ""),
        (13.88, ""),
        (14.98, ""),
        (14.73, ""),
        (13.00, ""),
        (18.74, ""),
        (15.74, ""),
        (17.14, ""),
        (16.60, ""),
        (18.27, ""),
        (13.77, ""),
        (15.42, ""),
        (15.63, ""),
        (16.07, ""),
        (18.22, ""),
        (13.41, ""),
        (17.81, ""),
        (19.69, ""),
        (14.50, ""),
        (16.61, ""),
        (13.36, ""),
        (14.02, ""),
        (16.58, ""),
        (19.80, ""),
        (14.71, ""),
        (19.85, ""),
        (17.15, ""),
        (18.70, ""),
        (15.27, ""),
        (11.69, ""),
        (18.18, ""),
        (13.47, ""),
        (17.26, ""),
        (18.21, ""),
        (23.90, ""),
        (38.65, ""),
        (22.88, ""),
        (15.36, ""),
        (17.57, ""),
        (18.73, ""),
        (14.08, ""),
        (17.24, ""),
        (16.99, ""),
        (16.49, ""),
        (17.71, ""),
        (19.31, ""),
        (14.84, ""),
        (13.08, ""),
        (16.10, ""),
        (18.43, ""),
        (16.18, ""),
        (15.24, ""),
        (15.72, ""),
        (18.35, ""),
        (16.28, ""),
        (14.11, ""),
        (15.52, ""),
        (18.44, ""),
        (14.81, ""),
        (17.68, ""),
        (16.04, ""),
        (14.73, ""),
        (13.58, ""),
        (17.51, ""),
        (14.70, ""),
    ]
    assert calculate_ao(solves, 100) == 15.601444444444446


if __name__ == "__main__":
    test_my_round()
    test_calculate_ao_no_solves()
    test_calculate_ao_5()
    test_calculate_ao_12()
    test_calculate_ao_100()
