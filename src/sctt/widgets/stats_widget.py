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
        self.add_columns("no.", "time", "ao5", "ao12")  # header

    def update(self, solves: list[tuple[Any, ...]]) -> None:
        self.clear()

        num_solves: int = len(solves)
        solve_ids: list[Any] = [solve[0] for solve in solves]

        df: pd.DataFrame = pd.DataFrame()
        df["time"] = [solve[1] for solve in solves]
        df["ao5"] = df["time"].rolling(window=5).apply(calculate_ao, raw=True)
        df["ao12"] = df["time"].rolling(window=12).apply(calculate_ao, raw=True)

        df = df.map(Timer().format_time, na_action="ignore")
        df = df.fillna("-")

        df["no."] = list(range(1, num_solves + 1))
        df = df.loc[:, ["no.", "time", "ao5", "ao12"]]

        df = df[::-1]  # 逆順にする

        for solve_id, row in zip(
            solve_ids, df.itertuples(index=False, name=None), strict=False
        ):
            styled_row = [Text(str(cell), justify="center") for cell in row]
            self.add_row(*styled_row, key=solve_id)
