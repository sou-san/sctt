import time

from pytest import MonkeyPatch

from sctt.modules.timer import Timer, TimerState


def test_initial_state() -> None:
    """初期化時のステートや属性を確認"""

    timer: Timer = Timer()

    assert timer.state == TimerState.STOPPED
    assert timer.get_elapsed_time() == Timer.INIT_TIME


def test_on_press_to_waiting_for_start(monkeypatch: MonkeyPatch) -> None:
    """STOPPED 状態から on_press で WAITING_FOR_START に移行"""

    timer: Timer = Timer()
    fake_time: float = 100.0  # 正規化された時間
    monkeypatch.setattr(time, "perf_counter", lambda: fake_time)

    timer.on_press()

    assert timer.state == TimerState.WAITING_FOR_START


def test_on_press_to_ready_to_start(monkeypatch: MonkeyPatch) -> None:
    """WAITING_FOR_START で持続時間が満たされた場合"""

    timer: Timer = Timer()
    monkeypatch.setattr(time, "perf_counter", lambda: 0.0)

    timer.on_press()

    assert timer.state == TimerState.WAITING_FOR_START

    # 持続時間が waiting_time を超える
    monkeypatch.setattr(time, "perf_counter", lambda: timer.waiting_time + 0.1)
    timer.on_press()

    assert timer.state == TimerState.READY_TO_START


def test_on_release_to_running(monkeypatch: MonkeyPatch) -> None:
    """READY_TO_START の状態から on_release で RUNNING に移行"""

    timer: Timer = Timer()
    monkeypatch.setattr(time, "perf_counter", lambda: 0.0)

    timer.on_press()
    timer.state = TimerState.READY_TO_START  # ダイレクトにREADY_TO_STARTにする

    fake_start_time: float = 50.0
    monkeypatch.setattr(time, "perf_counter", lambda: fake_start_time)
    timer.on_release()

    assert timer.state == TimerState.RUNNING
    assert timer._start_time == fake_start_time


def test_calculate_elapsed_time_running(monkeypatch: MonkeyPatch) -> None:
    """RUNNING の状態での経過時間の計算"""

    timer: Timer = Timer()
    start_time: float = 100.0
    monkeypatch.setattr(time, "perf_counter", lambda: start_time)
    timer.state = TimerState.RUNNING
    timer._start_time = start_time

    # 5秒経過
    monkeypatch.setattr(time, "perf_counter", lambda: start_time + 5)
    elapsed_time = timer.get_elapsed_time()

    assert elapsed_time == 5.0


def test_calculate_elapsed_time_maximum(monkeypatch: MonkeyPatch) -> None:
    """経過時間が MAXIMUM_TIME を超えないか確認"""

    timer: Timer = Timer()
    start_time: float = 100.0
    monkeypatch.setattr(time, "perf_counter", lambda: start_time)
    timer.state = TimerState.RUNNING
    timer._start_time = start_time

    # 最大値+10秒経過
    monkeypatch.setattr(time, "perf_counter", lambda: start_time + Timer.MAXIMUM_TIME + 10)
    elapsed_time: float = timer.get_elapsed_time()

    assert elapsed_time == Timer.MAXIMUM_TIME


def test_format_time() -> None:
    """format_time メソッドのフォーマット確認"""

    timer: Timer = Timer()

    assert timer.format_time(0) == "0.00"
    assert timer.format_time(65.1234) == "1:05.12"
    assert timer.format_time(3605.5678) == "1:00:05.57"
    assert timer.format_time(1376.92586) == "22:56.93"


def test_format_time_with_timer_state() -> None:
    """RUNNING 状態では小数一位、その他では小数二位のフォーマット確認"""

    timer: Timer = Timer()

    timer.state = TimerState.STOPPED

    assert timer.format_time(65.1234, timer_state=True) == "1:05.12"

    timer.state = TimerState.WAITING_FOR_START

    assert timer.format_time(65.1234, timer_state=True) == "1:05.12"

    timer.state = TimerState.READY_TO_START

    assert timer.format_time(65.1234, timer_state=True) == "1:05.12"

    timer.state = TimerState.RUNNING

    assert timer.format_time(65.1234, timer_state=True) == "1:05.1"
