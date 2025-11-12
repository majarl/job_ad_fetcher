from datetime import datetime, timezone

from .fetch_result import FetchResult
from .jobnet_connector import get_ads


class SearchParams:
    page_size: int
    page_number: int
    search_terms: str
    km_radius: int
    postal_code: int
    sort_by: str

    def __init__(
            self,
            page_size: int,
            page_number: int,
            search_terms: str,
            km_radius: int,
            postal_code: int,
            sort_by: str = "PublicationDate"
    ):
        self.page_size = page_size
        self.page_number = page_number
        self.search_terms = search_terms
        self.km_radius = km_radius
        self.postal_code = postal_code
        self.sort_by = sort_by

    def __repr__(self):
        return f"""SearchParams:
        {self.page_size=}
        {self.page_number=}
        {self.search_terms=}
        {self.km_radius=},
        {self.postal_code},
        {self.sort_by}
        """

    def to_params(self):
        params = {
            "resultsPerPage" : self.page_size,
            "pageNumber" : self.page_number,
            "orderType": self.sort_by,
            "searchString": self.search_terms,
        }
        if self.km_radius > -1: params["kmRadius"] = self.km_radius
        if self.postal_code > -1: params["postalCode"] = self.postal_code
        return params

    @classmethod
    def from_search_params_alter_page_number(cls, search_params, new_page_number):
        return cls(
            page_size=search_params.page_size,
            page_number=new_page_number,
            search_terms=search_params.search_terms,
            km_radius=search_params.km_radius,
            postal_code=search_params.postal_code,
            sort_by=search_params.sort_by
        )


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
