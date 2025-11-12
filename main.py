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



if __name__ == "__main__":
    do_search()
