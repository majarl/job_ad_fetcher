import sqlite3
import os
from datetime import datetime
from pprint import pprint

from ad_model.db_operations_sqlite import clean_db, install_db, insert_job_ad_row
from ad_model.job_ad import JobAd


def test_job_ad():
    print(__file__)
    job_ad_1 = JobAd("Sweden",
                      "19000",
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "123",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now())
    print(job_ad_1)
    json_str = job_ad_1.to_json()
    job_ad_1_back: JobAd = JobAd.from_json(json_str)
    print(job_ad_1_back)
    assert(job_ad_1_back.job_ad_id == "123")


def try_database():
    db_file = "try.db"
    clean_db(db_file)
    install_db(db_file)


def try_insert_data():
    job_ad_1 = JobAd("Sweden",
                      "19000",
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "123",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now())
    pprint(job_ad_1.to_db_ready())
    conn = sqlite3.connect("try.db")
    insert_job_ad_row(conn, job_ad_1)


def try_reading_data():
    conn = sqlite3.connect("try.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    result = cursor.execute("""
    SELECT * FROM job_ads
    WHERE job_ad_id = '123'
    """)
    job_ads = result.fetchall()
    for ja in job_ads:
        print(ja["country"])
        print(ja.keys())


def try_inserting_duplicates():
    job_ad_1 = JobAd("Sweden",
                      "19000",
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "123",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now())
    job_ad_2 = JobAd("Norway",
                      "19000",
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "123",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now())
    with sqlite3.connect("try.db") as conn:
        conn.row_factory = sqlite3.Row
        insert_job_ad_row(conn, job_ad_1)
        insert_job_ad_row(conn, job_ad_2)
        print(f"""Has inserted:
        f{job_ad_1=}
        f{job_ad_2=}
        """)






if __name__ == "__main__":
    test_job_ad()
    try_database()
    try_insert_data()
    try_reading_data()
    try_inserting_duplicates()