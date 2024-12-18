from pathlib import Path

from xdg_base_dirs import xdg_cache_home, xdg_data_home


def get_sctt_dir(root: Path) -> Path:
    dir: Path = root / "sctt"
    dir.mkdir(parents=True, exist_ok=True)

    return dir


def get_cache_dir() -> Path:
    return get_sctt_dir(xdg_cache_home())


def get_data_dir() -> Path:
    return get_sctt_dir(xdg_data_home())


def get_cache_file() -> Path:
    file: Path = get_cache_dir() / "sctt_last_session_id.txt"
    file.touch(exist_ok=True)

    return file


def get_database_file() -> Path:
    file: Path = get_data_dir() / "sctt.db"
    file.touch(exist_ok=True)

    return file
