
import sys
from datetime import datetime, timezone
from typing import Any

import requests
import logging

from fetch_result import FetchResult


jobnet_url = "https://jobnet.dk/bff/FindJob/Search"

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def get_ads(
        n_ads: int = 10,
        page_number: int = 1,
        params=None
):
    if params is None: params = { }
    params["resultsPerPage"] = n_ads
    params["pageNumber"] = page_number
    params["orderType"] = "PublicationDate"

    result = requests.get(jobnet_url, params=params)
    log.info(f"GET from {result.url}: {result.status_code=}")

    if not result.ok:
        return FetchResult.error(f"ERROR: {result.text}, {result.status_code=}")
    else:
        return FetchResult.success(result.json())


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
    pass


def run():
    print("jobnet_connector test run...")
    params = {
        "searchString": "Java",
        # "kmRadius": "10",
        # "postalCode": "1650"
    }
    ads_result = get_ads(params=params)
    if not ads_result.ok():
        print(ads_result.msg)
        return

    ads, total, time = extract_ads(ads_result.payload)
    log.info(f"""
    Number of ads fetched: {len(ads)}
    total number of ads: {total}
    fetched at: {time}""");




if __name__ == "__main__":
    run()