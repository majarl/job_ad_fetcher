from datetime import datetime, timezone

from .fetch_result import FetchResult
from .search_params import SearchParams
from .jobnet_connector import get_ads


class SearchResult:
    fetch_result: FetchResult
    search_params: SearchParams
    time_of_search: datetime
    number_of_hits: int
    job_ads: list[dict]

    def __init__(self, fetch_result, params: SearchParams, time_of_search):
        self.fetch_result = fetch_result
        self.search_params = params
        self.time_of_search = time_of_search
        self.job_ads = fetch_result.payload["jobAds"]
        self.number_of_hits = fetch_result.payload["totalJobAdCount"]

    def __repr__(self):
        return f"""
        {self.search_params=}
        {self.time_of_search=}
        {self.number_of_hits=}
        {len(self.job_ads)}
        """


class AllSearchResults:
    search_results: list[SearchResult]
    pass






def search_ads(search_params: SearchParams) -> SearchResult | FetchResult:
    params = search_params.to_params()
    now = datetime.now(timezone.utc)

    fetch_result: FetchResult = get_ads(params)

    if not fetch_result.success:
        print(fetch_result)
        return fetch_result
    else:
        search_result: SearchResult = SearchResult(fetch_result, params, now)
        return search_result
