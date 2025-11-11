from .fetch_result import FetchResult
from datetime import datetime

class SearchResult:
    fetch_result: FetchResult
    params: dict
    time_of_search: datetime
    number_of_hits: int
    page_size: int
    page_number: int
    job_ads: list[dict]

    def __init__(self, fetch_result, params, time_of_search):
        self.fetch_result = fetch_result
        self.params = params
        self.time_of_search = time_of_search
        self.page_size = params["resultsPerPage"]
        self.page_number = params["pageNumber"]
        self.job_ads = fetch_result.payload["jobAds"]
        self.number_of_hits = fetch_result.payload["totalJobAdCount"]

    def __repr__(self):
        return f"""
        {self.params=}
        {self.time_of_search=}
        {self.number_of_hits=}
        {len(self.job_ads)}
        """
