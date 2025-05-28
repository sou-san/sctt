import math
from collections.abc import Iterable, Sequence
from typing import Any

from rich.text import Text

from sctt.modules.calculate_ao import calculate_ao
from sctt.modules.timer import Timer
from sctt.widgets.my_datatable import MyDataTable


class StatsWidget(MyDataTable[Text]):
    def __init__(self) -> None:
        super().__init__(cursor_type="cell", zebra_stripes=True)

    def on_mount(self) -> None:
        # header
        self.add_column("no.", key="no.")
        self.add_column("time", key="time")
        self.add_column("ao5", key="ao5")
        self.add_column("ao12", key="ao12")

    @staticmethod
    def _format_times(solves: Sequence[tuple[int, float, str]]) -> list[str]:
        result: list[str] = []

        for solve in solves:
            _, time, penalty = solve

            match penalty:
                case "":
                    result.append(Timer.format_time(time, 2))
                case "plus_2":
                    result.append(f"{Timer.format_time(time + 2, 2)}+")
                case "dnf":
                    result.append("DNF")
                case _:
                    raise ValueError(f"Invalid penalty: {penalty}")

        return result

    @staticmethod
    def _format_ao_values(solves: list[tuple[Any, ...]], n: int) -> list[str]:
        result: list[str] = []

        for i in range(1, len(solves) + 1):
            ao_value: float | str = calculate_ao(
                tuple(solve[1:] for solve in solves[i - n : i]), n
            )

            if isinstance(ao_value, float):
                if math.isnan(ao_value):
                    result.append("-")
                else:
                    result.append(Timer.format_time(ao_value, 2))
            else:
                result.append(str(ao_value))

        return result

    def update(self, solves: list[tuple[Any, ...]]) -> None:
        self.clear()

        num_solves: Iterable[str] = map(str, range(len(solves), 0, -1))
        times: Iterable[str] = reversed(self._format_times(solves))
        ao5_results: Iterable[str] = reversed(self._format_ao_values(solves, 5))
        ao12_results: Iterable[str] = reversed(self._format_ao_values(solves, 12))
        solve_ids: Iterable[str] = (str(solve[0]) for solve in reversed(solves))

        for num_solve, time, ao5, ao12, solve_id in zip(
            num_solves, times, ao5_results, ao12_results, solve_ids, strict=True
        ):
            self.add_row(
                Text(num_solve, justify="center"),
                Text(time, justify="center"),
                Text(ao5, justify="center"),
                Text(ao12, justify="center"),
                key=solve_id,
            )

        # cache_info = calculate_ao.cache_info()
        # hit_rate = (
        #     cache_info.hits / total * 100
        #     if (total := (cache_info.hits + cache_info.misses))
        #     else 0.0
        # )
        # self.log.debug(
        #     f"calculate_ao() cache info: {cache_info}, cache hit rate: {hit_rate:.2f}%"
        # )
