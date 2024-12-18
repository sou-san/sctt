from sctt.app import Sctt
from sctt.locations import get_database_file
from sctt.modules.database import Database


def main() -> None:
    db: Database = Database(get_database_file())
    Sctt(db).run()


if __name__ == "__main__":
    main()
