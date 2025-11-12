from datetime import datetime, timezone

from .fetch_result import FetchResult
from .search_params import SearchParams


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

