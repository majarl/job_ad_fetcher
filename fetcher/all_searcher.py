from fetcher.jobnet_connector import search_ads
from fetcher.search_params import SearchParams
from fetcher.search_result import SearchResult
from fetcher.fetch_result import FetchResult
import math


class AllSearcher:
    search_results: list[SearchResult] = []
    number_of_pages = 0

    def search_first_batch(self, params: SearchParams) -> SearchResult | FetchResult:
        self.print_progress(params)
        result = search_ads(params)
        if isinstance(result, SearchResult):
            self.search_results.append(result)
            self.number_of_pages = math.ceil(result.number_of_hits / params.page_size)
            print("number_of_pages:", self.number_of_pages)
            print("     total hits:", result.number_of_hits)
        else:
            print(f"Warning: No valid result: {result}")
        return result

    def search_nexts(self, params: SearchParams, next_page):
        params.page_number = next_page
        self.print_progress(params)
        result = search_ads(params)
        if isinstance(result, SearchResult):
            self.search_results.append(result)
        else:
            print(f"Warning: No valid result: {result}")

    def search_all(self, params: SearchParams):
        search_result = self.search_first_batch(params)
        if search_result.number_of_hits <= 0:
            return self.search_results
        for i in range(2, self.number_of_pages + 1):
            self.search_nexts(params, i)
        print(f"Done. Got {len(self.search_results)}")

    def print_progress(self, params: SearchParams, msg: str = ""):
        print(f" >>> {params.page_number} ({self.number_of_pages}) :")

    def get_all_job_ads(self):
        combined = []
        for sr in self.search_results:
            ads = sr.job_ads
            combined.extend(ads)
        return combined

