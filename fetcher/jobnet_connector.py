import logging
import sys
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import requests

from .fetch_result import FetchResult
from .search_params import SearchParams
from .search_result import SearchResult


jobnet_url = "https://jobnet.dk/bff/FindJob/Search"
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def get_ads(params: dict = None):
    """Concrete execution of GET request of jobnet search endpoint.
    :type params: Dictionary of request parameters generated with
            SearchParameter.to_params()."""
    if params is None: params = { }

    result = requests.get(jobnet_url, params=params)
    log.info(f"GET from {result.url}: {result.status_code=}")

    if not result.ok:
        return FetchResult.error(f"ERROR: {result.text}, {result.status_code=}")
    else:
        return FetchResult.success(result.json())


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




def extract_ads(ad_dict: dict) -> tuple[Any, Any, datetime]:
    """Extracts the actual ads from response that also includes
    things like facets and more.

    :param ad_dict: a response dictionary from jobnet.
    :return: tuple with
        - jobAds list
        - total number of found ads
        - extraction time
    """
    return (ad_dict["jobAds"],
            ad_dict["totalJobAdCount"],
            datetime.now(timezone.utc))


def display_ads(ad_list: list[dict[Any]]):
    desired_columns = [
        "postalCode",
        "postalDistrictName",
        "hiringOrgName",
        "occupation",
        "jobAdUrl",
        "title",
        "workPlaceAddress"
    ]
    df = pd.DataFrame(ad_list)
    print(df[desired_columns])




