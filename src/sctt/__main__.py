from sctt.app import Sctt
from sctt.locations import get_database_file
from sctt.modules.database import Database


def main() -> None:
    try:
        db: Database = Database(get_database_file())
    except PermissionError:
        print("You must be root to use sctt on linux.\n\nsudo -E $(which sctt)")
    else:
        Sctt(db).run()


if __name__ == "__main__":
    main()
