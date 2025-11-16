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
    for idx, ad in enumerate(all_ads):
        pprint(f"{idx}: {ad["hiringOrgName"]} {ad["title"]} {ad["occupation"]}")






if __name__ == "__main__":
    do_all_search()
