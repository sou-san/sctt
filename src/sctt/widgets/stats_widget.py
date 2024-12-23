from typing import Any

import pandas as pd
from rich.text import Text
from textual.widgets import DataTable

from sctt.modules.calculate_ao import calculate_ao
from sctt.modules.timer import Timer


class StatsWidget(DataTable[Text]):
    def on_mount(self) -> None:
        self.cursor_type = "none"
        self.zebra_stripes = True

        # header
        self.add_column("no.", key="no.")
        self.add_column("time", key="time")
        self.add_column("ao5", key="ao5")
        self.add_column("ao12", key="ao12")

    def update(self, solves: list[tuple[Any, ...]]) -> None:
        self.clear()

        num_solves: int = len(solves)

        df: pd.DataFrame = pd.DataFrame()
        df["time"] = [solve[1] for solve in solves]
        df["ao5"] = df["time"].rolling(window=5).apply(calculate_ao, raw=True)
        df["ao12"] = df["time"].rolling(window=12).apply(calculate_ao, raw=True)

        df = df.map(Timer().format_time, na_action="ignore")
        df = df.fillna("-")

        df["no."] = list(range(1, num_solves + 1))
        df = df.loc[:, ["no.", "time", "ao5", "ao12"]]

        # 逆順にする
        df = df[::-1]
        solve_ids: list[int] = list(reversed([int(solve[0]) for solve in solves]))

        for solve_id, row in zip(
            solve_ids, df.itertuples(index=False, name=None), strict=True
        ):
            styled_row = [Text(str(cell), justify="center") for cell in row]
            self.add_row(*styled_row, key=str(solve_id))
