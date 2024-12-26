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

    def get_elapsed_time(self) -> float:
        match self.state:
            case TimerState.STOPPED:
                return self._elapsed_time
            case TimerState.WAITING_FOR_START:
                return self._elapsed_time
            case TimerState.READY_TO_START:
                return self.INIT_TIME
            case TimerState.RUNNING:
                self._elapsed_time = time.perf_counter() - self._start_time
                return min(self._elapsed_time, self.MAXIMUM_TIME)

    @staticmethod
    def _convert_seconds_to_hms(seconds: float) -> tuple[float, float, float]:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return h, m, s

    @staticmethod
    def _format_time_accuracy(total_seconds: float, decimal_places: int) -> str:
        """
        Args:
            decimal_places: 小数点第何位まで表示するかを指定する。
        """

        init_time: float = 0.0
        hours, minutes, seconds = Timer._convert_seconds_to_hms(total_seconds)

        if hours:
            return (
                f"{hours:.0f}:{minutes:02.0f}:{seconds:0{3+decimal_places}.{decimal_places}f}"
            )
        elif minutes:
            return f"{minutes:.0f}:{seconds:0{3+decimal_places}.{decimal_places}f}"
        elif seconds:
            return f"{seconds:.{decimal_places}f}"
        else:
            return f"{init_time:.0{decimal_places}f}"

    def format_time(
        self,
        elapsed_time: float,
        decimal_places: int = 2,
        timer_state: bool = False,
    ) -> str:
        """
        フォーマットされたタイムの文字列を返す関数

        Args:
            time: フォーマットするタイムを指定する。
            decimal_places: 小数点第何位までか指定する。
            timer_state: タイマーの状態によって動的にフォーマットするかどうかを指定する。
        """

        if timer_state:
            match self.state:
                case TimerState.RUNNING:
                    return Timer._format_time_accuracy(elapsed_time, 1)
                case _:
                    return Timer._format_time_accuracy(elapsed_time, 2)
        else:
            return Timer._format_time_accuracy(elapsed_time, decimal_places)
