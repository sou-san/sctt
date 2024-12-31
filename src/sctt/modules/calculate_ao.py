import math


def my_round(x: float, decimals: int = 0) -> float:
    return float(math.floor(x * 10**decimals + 0.5) / 10**decimals)


def _sort_solves(solves: list[tuple[float, str]]) -> list[tuple[float, str]]:
    """ペナルティを考慮してソルブをソートする関数

    ペナルティが +2 の場合は 2 を足してソートされる。
    ペナルティが DNF の場合は最遅のソルブとしてソートされ、
    DNF が複数ある場合は、それらのタイムがさらにソートされる。
    """

    valid_solves: list[tuple[float, str]] = []
    dnf_solves: list[tuple[float, str]] = []

    for solve in solves:
        match solve[1]:
            case "":
                valid_solves.append(solve)
            case "plus_2":
                valid_solves.append((solve[0] + 2, solve[1]))
            case "dnf":
                dnf_solves.append(solve)
            case _:
                pass

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

    times: list[float] = [solve[0] for solve in trimmed_window]
    return my_round(sum(times), 2) / my_round(len(trimmed_window), 2)
