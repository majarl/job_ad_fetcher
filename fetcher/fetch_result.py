from typing import Any
from datetime import datetime


class FetchResult:
    success: bool
    msg: str
    payload: Any
    exception: Exception | None

    def __init__(self,
                 success: bool = False,
                 msg: str = "Empty",
                 payload: Any = None,
                 exception: Exception | None  = None):
        self.success = success
        self.msg = msg
        self.payload = payload
        self.exception = exception

    def __repr__(self):
        return f"""FetchResult:
        {self.success=}
        {self.msg=}
        {self.payload=}
        {self.exception=}
        """

    def ok(self):
        return self.success

    def failed(self):
        return not self.success

    @staticmethod
    def success(payload: Any):
        return FetchResult(
            success=True,
            msg="Ok",
            payload=payload,
            exception=None
        )

    @staticmethod
    def error(msg: str, exception: Exception | None = None):
        return FetchResult(
            success=False,
            msg=msg,
            payload=None,
            exception=exception
        )


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
