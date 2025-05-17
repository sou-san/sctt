import math
from collections.abc import Iterator


def _sort_solves(solves: list[tuple[float, str]]) -> list[tuple[float, str]]:
    """ペナルティを考慮してソルブをソートする関数

    ペナルティが +2 の場合は 2 を足してソートされる。
    ペナルティが DNF の場合は最遅のソルブとしてソートされ、
    DNF が複数ある場合は、それらのタイムがさらにソートされる。
    """

    valid_solves: list[tuple[float, str]] = []
    dnf_solves: list[tuple[float, str]] = []

    for solve in solves:
        time, penalty = solve

        match penalty:
            case "":
                valid_solves.append(solve)
            case "plus_2":
                valid_solves.append((time + 2, penalty))
            case "dnf":
                dnf_solves.append(solve)
            case _:
                raise ValueError(f"Invalid penalty: {penalty}")

    valid_solves.sort()
    dnf_solves.sort()

    return valid_solves + dnf_solves


def calculate_ao(solves: list[tuple[float, str]], n: int) -> float | str:
    if len(solves) != n:
        return float("nan")

    trim_count: int = int(math.ceil(n * 0.05))
    sorted_window: list[tuple[float, str]] = _sort_solves(solves)
    trimmed_window: list[tuple[float, str]] = sorted_window[
        trim_count : len(solves) - trim_count
    ]

    if len(trimmed_window) < max(0, n - (trim_count * 2)):
        return float("nan")

    if trimmed_window[-1][1] == "dnf":
        return "DNF"

    times: Iterator[float] = (solve[0] for solve in trimmed_window)
    return sum(times) / len(trimmed_window)
