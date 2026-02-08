from src.database.engine import create_db_and_tables


def run_migrations():
    print("Running migrations...")
    create_db_and_tables()
    print("Done!")


if __name__ == "__main__":
    run_migrations()
