import sqlite3

from ad_model.db_operations_sqlite import insert_multiple_job_ads
from ad_model.job_ad import JobAd
from ad_model.search_event import SearchEvent
from config import db_name
from fetcher.all_searcher import AllSearcher
from fetcher.jobnet_connector import search_ads
from fetcher.search_result import SearchParams
from pprint import pprint

def do_search():
    search_params = SearchParams(
        10,
        1,
        "Python",
        10,
        1650
    )
    r = search_ads(search_params)
    print(r)


def create_search_params():
    sp_0 = SearchParams(
        10,
        1,
        "Python",
        10,
        1650
    )
    print(sp_0)
    sp_1 = SearchParams.from_search_params_alter_page_number(sp_0, 2)
    print(sp_1)
    pprint(sp_1.to_params())

    sp_2 = SearchParams(
        10,
        1,
        "Python",
        -1,
        -1
    )
    pprint(sp_2.to_params())


def save_scraping(se: SearchEvent, job_ad_list: [JobAd]):
    print(f"\n ---- Attempting to save job ads for search event ----")
    print(f" search_event: {se} containing {len(job_ad_list)} job ads.\n")
    with sqlite3.connect(db_name) as conn:
        num_inserted = insert_multiple_job_ads(conn, job_ad_list)
        print(f"{num_inserted=}")


def do_all_search():
    all_searcher = AllSearcher()
    sp = SearchParams(
        10,
        1,
        "Python",
        10,
        1650
    )
    search_event = all_searcher.search_all(sp)
    print(len(all_searcher.search_results))
    print(search_event)

    all_ads = all_searcher.get_all_job_ads()
    save_scraping(search_event, all_ads)






if __name__ == "__main__":
    do_all_search()
