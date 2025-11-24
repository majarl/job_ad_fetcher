import sqlite3
import os
from datetime import datetime
from pprint import pprint

from ad_model.db_operations_sqlite import clean_db, install_db, insert_job_ad_row, insert_multiple_job_ads, \
    insert_search_event, insert_search_event_rel_job_ad
from ad_model.job_ad import JobAd
from ad_model.search_event import SearchEvent, SearchEventRelationJobAd


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


def try_from_dict():
    a_dict = {'applicationDeadline': '2025-12-14T00:00:00+01:00',
              'applicationDeadlineStatus': 'ExpirationDate',
              'conceptUriDa': 'http://data.star.dk/esco/occupation/7e96834b-070c-43d7-b826-8d396bd02b21',
              'country': 'Danmark',
              'cvr': '29190623',
              'description': 'something textual',
              'hasLogo': True,
              'hiringOrgName': 'Frederiksberg Hospital',
              'isFavorite': False,
              'isSeen': False,
              'jobAdId': '14380ab9-60d6-4a70-91ae-6005b8612f17',
              'jobAdUrl': '',
              'occupation': 'Biomediciner',
              'postalCode': 2400,
              'postalDistrictName': 'København NV',
              'publicationDate': '2025-11-20T00:00:00+01:00',
              'title': 'Senior Mass Spectrometry Specialist',
              'workHourPartTime': False,
              'workPlaceAddress': ''}
    job_ad = JobAd.from_dict(a_dict)
    print(job_ad)


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


def try_inserting_multiple():
    job_ads = [JobAd("Sweden",
                      "19000",
                      "Göteborg",
                      "Izzted",
                      "Coder",
                      "1",
                      "http:localhost",
                      "NoWhere",
                      800000,
                      "Hacker",
                      "Lorem Ipsum",
                      datetime.now(),
                      "some status",
                      datetime.now()),
               JobAd("Sweden",
                     "19000",
                     "Göteborg",
                     "Izzted",
                     "Software developer",
                     "2",
                     "http:localhost",
                     "NoWhere",
                     800000,
                     "Hacker",
                     "Lorem Ipsum",
                     datetime.now(),
                     "some status",
                     datetime.now()),
               ]
    with sqlite3.connect("try.db") as conn:
        insert_multiple_job_ads(conn, job_ads)
        res = conn.cursor().execute("""SELECT * FROM job_ads""")
        print(len(res.fetchall()))


def try_insert_search_event():
    print("---------------------")
    se = SearchEvent(se_id=-1,
                     search_terms="Java",
                     km_radius=10,
                     postal_code=1650,
                     number_of_results=42,
                     at_time=datetime.now())
    pprint(se.to_db_ready())
    with sqlite3.connect("try.db") as conn:
        conn.row_factory = sqlite3.Row
        insert_search_event(conn, se)
        res = conn.cursor().execute("SELECT * FROM search_events;")
        for r in res.fetchall():
            print(r.keys())
            print(f"{r["se_id"]}, {r["search_terms"]}, {r["at_time"]}")


def try_insert_search_event_rel():
    print("---------------------")
    serel = SearchEventRelationJobAd(
        rel_id=-1,
        se_id=1,
        job_ad_id="something"
    )
    with sqlite3.connect("try.db") as conn:
        conn.row_factory = sqlite3.Row
        insert_search_event_rel_job_ad(conn, serel)
        res = conn.cursor().execute("SELECT * FROM search_event_job_ad;")
        for r in res.fetchall():
            print(r.keys())
            print(f"{r["rel_id"]}, {r["se_id"]}, {r["job_ad_id"]}")




if __name__ == "__main__":
    test_job_ad()
    try_from_dict()
    try_database()
    try_insert_data()
    try_reading_data()
    try_inserting_duplicates()
    try_inserting_multiple()
    try_insert_search_event()
    try_insert_search_event_rel()