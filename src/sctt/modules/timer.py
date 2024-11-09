from __future__ import annotations

import time
from enum import Enum, auto


class TimerState(Enum):
    STOPPED = auto()
    WAITING_FOR_START = auto()
    READY_TO_START = auto()
    RUNNING = auto()


class Timer:
    INIT_TIME: float = 0.0
    MAXIMUM_TIME: float = 35_999.99  # 9:59:59.99

    def __init__(self) -> None:
        self.waiting_time: float = 0.3
        self.state: TimerState = TimerState.STOPPED
        self._start_time: float = 0.0
        self._elapsed_time: float = 0.0
        self._hours: float = 0.0
        self._minutes: float = 0.0
        self._seconds: float = 0.0
        self._press_time: float = 0.0
        self._was_key_released_after_stop: bool = False

    def on_press(self) -> None:
        match self.state:
            case TimerState.STOPPED:
                self._press_time = time.perf_counter()
                self.state = TimerState.WAITING_FOR_START
            case TimerState.WAITING_FOR_START:
                if self._check_hold_duration() and not self._was_key_released_after_stop:
                    self.state = TimerState.READY_TO_START
            case TimerState.READY_TO_START:
                pass
            case TimerState.RUNNING:
                self.state = TimerState.STOPPED
                self._was_key_released_after_stop = True

    def on_release(self) -> None:
        match self.state:
            case TimerState.STOPPED:
                self._was_key_released_after_stop = False
            case TimerState.WAITING_FOR_START:
                self.state = TimerState.STOPPED
                self._was_key_released_after_stop = False
            case TimerState.READY_TO_START:
                if not self._was_key_released_after_stop:
                    self.state = TimerState.RUNNING
                    self._start_time = time.perf_counter()
                else:
                    self.state = TimerState.STOPPED
            case TimerState.RUNNING:
                pass

    def _check_hold_duration(self) -> bool:
        return time.perf_counter() - self._press_time >= self.waiting_time

    def _get__elapsed_time(self) -> float:
        return time.perf_counter() - self._start_time

    def format_time(self) -> str:
        """動的にフォーマットされたタイムの文字列を返す関数"""

        self._hours, self._minutes, self._seconds = self._get_h_m_s()

        match self.state:
            case TimerState.RUNNING:
                return self._format_time_accuracy(1)
            case _:
                return self._format_time_accuracy(2)

    def _get_h_m_s(self) -> tuple[float, float, float]:
        match self.state:
            case TimerState.RUNNING:
                self._elapsed_time = self._get__elapsed_time()
                if self._elapsed_time >= self.MAXIMUM_TIME:
                    self._elapsed_time = self.MAXIMUM_TIME
            case _:
                pass

        self._minutes, self._seconds = divmod(self._elapsed_time, 60)
        self._hours, self._minutes = divmod(self._minutes, 60)

        return self._hours, self._minutes, self._seconds

    def _format_time_accuracy(self, decimal_places: int) -> str:
        """
        Args:
            decimal_places: 小数点第何位まで表示するかを指定する。
        """

        match self.state:
            case TimerState.READY_TO_START:
                return f"{self.INIT_TIME:.0{decimal_places}f}"
            case _:
                if self._hours:
                    return f"{self._hours:.0f}:{self._minutes:02.0f}:{self._seconds:0{3+decimal_places}.{decimal_places}f}"
                elif self._minutes:
                    return f"{self._minutes:.0f}:{self._seconds:0{3+decimal_places}.{decimal_places}f}"
                elif self._seconds:
                    return f"{self._seconds:<{3+decimal_places}.{decimal_places}f}"

                return f"{self.INIT_TIME:.0{decimal_places}f}"
