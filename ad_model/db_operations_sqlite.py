import os
import sqlite3

from ad_model.job_ad import JobAd


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
    cursor.execute(JobAd.create_table_statement())
    res = cursor.execute("PRAGMA table_info('job_ads')")
    columns = res.fetchall()
    for c in columns:
        print(c)


def insert_job_ad_row(conn: sqlite3.Connection, job_ad: JobAd):
    row, cols, placeholders = job_ad.to_db_ready()
    sql = f"""
    INSERT INTO job_ads ({cols}) 
    VALUES ({placeholders})  
    """
    cursor = conn.cursor()
    cursor.execute(sql, tuple(row.values()))
    conn.commit()
    print(f"Committed: {job_ad}")

