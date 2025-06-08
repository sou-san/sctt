import functools
import math
from collections.abc import Iterator, Sequence
from typing import Literal


def _sort_solves(solves: Sequence[tuple[float, str]]) -> list[tuple[float, str]]:
    """ペナルティを考慮してソルブをソートする。

    ペナルティが plus_2 の場合は 2 を足してソートされる。
    ペナルティが dnf の場合は最も遅いソルブとしてソートされる。
    dnf が複数ある場合は、それらのタイムがさらにソートされる。

    Args:
        solves (Sequence[tuple[float, str]]): タイムとペナルティを要素に持つタプルを要素に持つシーケンス。(ペナルティ: "" | "plus_2" | "dnf")
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


@functools.lru_cache(maxsize=10_000)
def calculate_ao(solves: Sequence[tuple[float, str]]) -> float | Literal["DNF"]:
    """Average of N を計算する。 (N は solves の個数)

    Args:
        solves (Sequence[tuple[float, str]]): タイムとペナルティを要素に持つタプルを要素に持つシーケンス。(ペナルティ: "" | "plus_2" | "dnf")
    """

    if (n := len(solves)) <= 2:
        return float("nan")

    trim_count: int = int(math.ceil(n * 0.05))
    sorted_solves: list[tuple[float, str]] = _sort_solves(solves)
    trimmed_solves: list[tuple[float, str]] = sorted_solves[trim_count : n - trim_count]

    # ペナルティを考慮してソートしたあと、トリムするから最も遅いソルブのペナルティが dnf なら ao N の値も DNF になる。
    if trimmed_solves[-1][-1] == "dnf":
        return "DNF"

    times: Iterator[float] = (time for time, _ in trimmed_solves)
    return sum(times) / len(trimmed_solves)
