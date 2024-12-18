from pathlib import Path
from typing import Any

import pytest

from sctt.modules.database import Database


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Path:
    """一時的なデータベースファイルを作成する"""

    return tmp_path / "sctt_pytest.db"


@pytest.fixture
def db(temp_db_path: Path) -> Database:
    """テスト用のDatabaseインスタンスを作成"""

    return Database(temp_db_path)


def test_create_session(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    assert session_id is not None, "セッションが正常に作成されるべき"

    sessions: list[tuple[Any, ...]] = db.get_all_sessions()

    assert len(sessions) == 1, "セッションは1つだけ存在するべき"
    assert sessions[0][1] == "Test Session", "セッション名が一致するべき"


def test_delete_session(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    if session_id is None:
        raise ValueError

    db.delete_session(session_id)

    sessions: list[tuple[Any, ...]] = db.get_all_sessions()

    assert len(sessions) == 0, "セッションが削除されるべき"


def test_add_solve(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    if session_id is None:
        raise ValueError

    solve_id: int | None = db.add_solve(12.34, "D2 R2 U2", session_id)

    assert solve_id is not None, "ソルブが正常に追加されるべき"

    solves: list[tuple[Any, ...]] = db.get_all_solves(session_id)

    assert len(solves) == 1, "ソルブは1つだけ存在するべき"

    assert solves[0][0] == solve_id, "ソルブのIDが一致するべき"
    assert solves[0][1] == session_id, "ソルブのセッションIDが一致するべき"
    assert solves[0][2] == 12.34, "ソルブのタイムが一致するべき"
    assert solves[0][3] == "D2 R2 U2", "ソルブのスクランブルが一致するべき"


def test_remove_solve(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    if session_id is None:
        raise ValueError

    solve_id: int | None = db.add_solve(12.34, "D2 R2 U2", session_id)

    if solve_id is None:
        raise ValueError

    db.remove_solve(solve_id, session_id)

    solves: list[tuple[Any, ...]] = db.get_all_solves(session_id)

    assert len(solves) == 0, "ソルブが削除されるべき"


def test_foreign_key_constraint(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    if session_id is None:
        raise ValueError

    db.add_solve(12.34, "D2 R2 U2", session_id)

    db.delete_session(session_id)

    sessions: list[tuple[Any, ...]] = db.get_all_sessions()

    assert len(sessions) == 0, "セッションが正常に削除されるべき"

    solves: list[tuple[Any, ...]] = db.get_all_solves(session_id)

    assert len(solves) == 0, "セッション削除時にソルブも削除されるべき"


def test_get_solve_times(db: Database) -> None:
    session_id: int | None = db.create_session("Test Session")

    if session_id is None:
        raise ValueError

    db.add_solve(12.34, "D2 R2 U2", session_id)
    db.add_solve(23.45, "D2 R2 U2", session_id)
    db.add_solve(34.56, "D2 R2 U2", session_id)

    solve_times: list[tuple[Any, ...]] = db.get_solve_ids_and_times(session_id)

    assert len(solve_times) == 3

    assert solve_times[0][0] == 1
    assert solve_times[1][0] == 2
    assert solve_times[2][0] == 3

    assert solve_times[0][1] == 12.34
    assert solve_times[1][1] == 23.45
    assert solve_times[2][1] == 34.56
