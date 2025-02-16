import math
from typing import Any

from rich.text import Text

from sctt.modules.calculate_ao import calculate_ao
from sctt.modules.timer import Timer
from sctt.widgets.my_datatable import MyDataTable


class StatsWidget(MyDataTable[Text]):
    def on_mount(self) -> None:
        self.cursor_type = "cell"
        self.zebra_stripes = True

        # header
        self.add_column("no.", key="no.")
        self.add_column("time", key="time")
        self.add_column("ao5", key="ao5")
        self.add_column("ao12", key="ao12")

    @staticmethod
    def _format_ao_values(solves: list[tuple[Any, ...]], n: int) -> list[str]:
        result: list[str] = []

        for i in range(1, len(solves) + 1):
            ao_value: float | str = calculate_ao([solve[1:] for solve in solves[i - n : i]], n)

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

        times: list[str] = []

        for solve in solves:
            match solve[2]:
                case "":
                    times.append(Timer.format_time(solve[1], 2))
                case "plus_2":
                    times.append(f"{Timer.format_time(solve[1] + 2, 2)}+")
                case "dnf":
                    times.append("DNF")
                case _:
                    raise ValueError(f"Invalid penalty: {solve[2]}")

        num_solves: list[int] = list(reversed(range(1, len(solves) + 1)))
        times = list(reversed(times))
        ao5_results: list[str] = list(reversed(self._format_ao_values(solves, 5)))
        ao12_results: list[str] = list(reversed(self._format_ao_values(solves, 12)))
        solve_ids: list[str] = list(reversed([str(solve[0]) for solve in solves]))

        for num_solve, time, ao5, ao12, solve_id in zip(
            num_solves, times, ao5_results, ao12_results, solve_ids, strict=True
        ):
            self.add_row(
                Text(str(num_solve), justify="center"),
                Text(time, justify="center"),
                Text(ao5, justify="center"),
                Text(ao12, justify="center"),
                key=solve_id,
            )
