import os
import sqlite3

from ad_model.job_ad import JobAd
from ad_model.search_event import SearchEvent, SearchEventRelationJobAd


def clean_db(db_file):
    print(f"Cleaning up file: {db_file}")
    try:
        os.remove(db_file)
        print(f"{db_file} is deleted.")
    except FileNotFoundError:
        print(f"File {db_file} not found.")
    except PermissionError:
        print(f"No permission to {db_file}.")


def install_db(db_file):
    print(f"Installing db in {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print("Creating job ad table...")
    cursor.execute(JobAd.create_table_statement())

    print("Creating search event table...")
    cursor.execute(SearchEvent.create_table_statement())

    print("Creating relations between job ads and search events...")
    cursor.execute(SearchEventRelationJobAd.create_table_statement())

    res = cursor.execute("PRAGMA table_info('job_ads')")
    columns = res.fetchall()
    for c in columns:
        print(c)


def insert_job_ad_row(conn: sqlite3.Connection, job_ad: JobAd):
    row, cols, placeholders = job_ad.to_db_ready()
    sql = f"""
    INSERT OR IGNORE INTO job_ads ({cols}) 
    VALUES ({placeholders})
    """
    cursor = conn.cursor()
    cursor.execute(sql, tuple(row.values()))
    conn.commit()
    print(f"Committed: {job_ad}")


def insert_multiple_job_ads(conn: sqlite3.Connection, job_ad_list: list[JobAd]) -> int:
    if len(job_ad_list) == 0:
        return 0

    rows = []
    for job_ad in job_ad_list:
        row, _, _ = job_ad.to_db_ready()
        rows.append(tuple(row.values()))
    row, cols, placeholders = job_ad_list[0].to_db_ready()

    cursor = conn.cursor()
    cursor.executemany(f"""
    INSERT OR IGNORE INTO job_ads ({cols})
    VALUES ({placeholders})
    """, rows)
    conn.commit()
    print(f"Commited {len(rows)} rows.")
    return len(rows)


def insert_search_event(conn: sqlite3.Connection, se: SearchEvent):
    row, cols, placeholders = se.to_db_ready()
    sql = f"""
    INSERT OR IGNORE INTO search_events ({cols})
    VALUES ({placeholders})
    """
    cursor = conn.cursor()
    cursor.execute(sql, tuple(row.values()))
    conn.commit()
    print(f"Commited: {se}")


def insert_search_event_rel_job_ad(conn: sqlite3.Connection, serel: SearchEventRelationJobAd):
    row, cols, placeholders = serel.to_db_ready()
    sql = f"""
    INSERT OR IGNORE INTO search_event_job_ad ({cols})
    VALUES ({placeholders})
    """

    cursor = conn.cursor()
    cursor.execute(sql, tuple(row.values()))
    conn.commit()
    print(f"Commited: {serel}")
