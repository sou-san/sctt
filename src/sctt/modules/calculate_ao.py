import math


def my_round(x: float, decimals: int = 0) -> float:
    return float(math.floor(x * 10**decimals + 0.5) / 10**decimals)


def calculate_ao(times: list[float]) -> float:
    n: int = len(times)
    trim_count: int = int(math.ceil(n * 0.05))
    sorted_window: list[float] = sorted(times)
    trimmed_window: list[float] = sorted_window[trim_count : n - trim_count]

    if len(trimmed_window) == 0:
        return float("nan")

    return my_round(my_round(sum(trimmed_window), 2) / len(trimmed_window), 2)
