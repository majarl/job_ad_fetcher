
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
logger = logging.getLogger(__name__)


def get_ads(
        n_ads: int = 10,
        page_number: int = 1,
        params=None
):
    if params is None: params = {
        "orderType": "PublicationDate",
    }

    params["resultsPerPage"] = n_ads
    params["pageNumber"] = page_number

    result = requests.get(jobnet_url, params=params)
    logger.info(f"GET from {result.url}: {result.status_code=}")

    if not result.ok:
        return FetchResult.error(f"ERROR: {result.text}, {result.status_code=}")
    else:
        return FetchResult.success(result.json())


def extract_ads(ad_dict: dict) -> tuple[Any, Any, datetime]:
    return (ad_dict["jobAds"],
            ad_dict["totalJobAdCount"],
            datetime.now(timezone.utc))



def run():
    print("jobnet_connector test run...")
    ads_result = get_ads()
    if ads_result.ok():
        ads, total, time = extract_ads(ads_result.payload)
        print(len(ads))
        print(total)
        print(time)
    else:
        print(ads_result.msg)



if __name__ == "__main__":
    run()