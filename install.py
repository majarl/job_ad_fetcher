from ad_model.db_operations_sqlite import install_db


def prepare_db(db_name: str):
    print(f" ----- Creating sqlite3 database {db_name} ------")
    install_db(db_name)


if __name__ == "__main__":
    install_db("searches.db")