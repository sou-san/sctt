import sqlite3
from pathlib import Path
from typing import Any


class Database:
    """データベースを管理するクラス

    ## テーブル例

    ### sessions table

    | id |    name   |      created_at     |      updated_at     |
    |:--:|:---------:|:-------------------:|:-------------------:|
    |  1 | session 1 | 2024-12-22 13:50:31 | 2024-12-22 17:15:12 |
    |  2 | session 2 | 2024-12-22 14:10:58 | 2024-12-22 14:10:58 |

    ### solves table

    | id | event |  time | penalty |                        scramble                       |         date        | session_id |
    |:--:|:-----:|:-----:|:-------:|:-----------------------------------------------------:|:-------------------:|:----------:|
    |  1 | 3x3x3 | 12.34 |   dnf   |  L2 F U B2 D F2 U' F2 U' L2 B2 L2 U' B' L' B F L F U2 | 2024-12-22 13:50:31 |      1     |
    |  2 | 2x2x2 |  5.67 |         |                 R F2 R' U F' U F2 R2 U'               | 2024-12-22 14:10:58 |      2     |
    |  3 | 3x3x3 | 11.82 |  plus_2 | U2 B2 L R U2 R U2 F2 L B2 U2 B2 D' B' D B' R2 D2 F2 U | 2024-12-22 17:15:12 |      1     |
    """

    def __init__(self, db_path: Path) -> None:
        self.db_path: Path = db_path

        self._create_sessions_table()
        self._create_solves_table()

    def _get_connection(self) -> sqlite3.Connection:
        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    def _create_sessions_table(self) -> None:
        query: str = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """

        with self._get_connection() as conn:
            conn.execute(query)

    def _create_solves_table(self) -> None:
        query: str = """
        CREATE TABLE IF NOT EXISTS solves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            time REAL NOT NULL,
            penalty TEXT NOT NULL,
            scramble TEXT NOT NULL,
            date TEXT NOT NULL,
            session_id INTEGER NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        );
        """

        with self._get_connection() as conn:
            conn.execute(query)

    def create_session(self, name: str) -> int | None:
        query: str = "INSERT INTO sessions (name, created_at, updated_at) VALUES (?, DATETIME('now'), DATETIME('now'));"

        with self._get_connection() as conn:
            return conn.execute(query, (name,)).lastrowid

    def delete_session(self, id: int) -> None:
        query: str = "DELETE FROM sessions WHERE id = ?;"

        with self._get_connection() as conn:
            conn.execute(query, (id,))

    def add_solve(
        self, event: str, time: float, scramble: str, session_id: int, penalty: str = ""
    ) -> int | None:
        query_solve: str = "INSERT INTO solves (event, time, penalty, scramble, date, session_id) VALUES (?, ?, ?, ?, DATETIME('now'), ?);"
        query_update: str = "UPDATE sessions SET updated_at = DATETIME('now') WHERE id = ?;"

        with self._get_connection() as conn:
            solve_id: int | None = conn.execute(
                query_solve, (event, time, penalty, scramble, session_id)
            ).lastrowid
            conn.execute(query_update, (session_id,))

            return solve_id

    def remove_solve(self, solve_id: int, session_id: int) -> None:
        query_delete: str = "DELETE FROM solves WHERE id = ?;"
        query_update: str = "UPDATE sessions SET updated_at = DATETIME('now') WHERE id = ?;"

        with self._get_connection() as conn:
            conn.execute(query_delete, (solve_id,))
            conn.execute(query_update, (session_id,))

    def get_session(self, id: int) -> list[tuple[Any, ...]]:
        query: str = "SELECT * FROM sessions WHERE id = ?;"

        with self._get_connection() as conn:
            return conn.execute(query, (id,)).fetchall()

    def get_solve(self, session_id: int, solve_id: int) -> tuple[Any, ...]:
        query: str = "SELECT * FROM solves WHERE session_id = ? AND id = ?;"

        with self._get_connection() as conn:
            return conn.execute(query, (session_id, solve_id)).fetchall()[0]

    def get_all_sessions(self) -> list[tuple[Any, ...]]:
        query: str = "SELECT * FROM sessions;"

        with self._get_connection() as conn:
            return conn.execute(query).fetchall()

    def get_all_solves(self, session_id: int) -> list[tuple[Any, ...]]:
        query: str = "SELECT * FROM solves WHERE session_id = ?;"

        with self._get_connection() as conn:
            return conn.execute(query, (session_id,)).fetchall()

    def get_solve_ids_and_times(self, session_id: int) -> list[Any]:
        query: str = "SELECT id, time FROM solves WHERE session_id = ?;"

        with self._get_connection() as conn:
            return conn.execute(query, (session_id,)).fetchall()
