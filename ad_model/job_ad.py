from dataclasses import dataclass, asdict
from datetime import datetime
import json
from typing import Any


@dataclass
class JobAd:
    country: str
    postal_code: str
    postal_district_name: str
    hiring_org_name: str
    occupation: str
    job_ad_id: str
    job_ad_url: str
    work_place_address: str
    cvr: int
    title: str
    description: str
    application_deadline: datetime
    application_deadline_status: str
    publication_date: datetime

    def to_json(self) -> str:
        return json.dumps(
            self.__dict__,
            default=lambda p: p.isoformat() if isinstance(p, datetime) else None)

    def to_db_ready(self) -> tuple[dict[str, int | None | Any], str, str]:
        def _transform_value(v):
            if v is None: return None
            if isinstance(v, bool): return 1 if v else 0
            if isinstance(v, datetime): return int(v.timestamp() * 1000)
            return v

        row = { key: _transform_value(value)
                for key, value in self.__dict__.items() }
        cols = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        return row, cols, placeholders


    @staticmethod
    def from_json(json_str: str):
        job_ad_json = json.loads(json_str)
        job_ad_json["application_deadline"] = datetime.fromisoformat(job_ad_json["application_deadline"])
        job_ad_json["publication_date"] = datetime.fromisoformat(job_ad_json["publication_date"])
        return JobAd(
            job_ad_json["country"],
            job_ad_json["postal_code"],
            job_ad_json["postal_district_name"],
            job_ad_json["hiring_org_name"],
            job_ad_json["occupation"],
            job_ad_json["job_ad_id"],
            job_ad_json["job_ad_url"],
            job_ad_json["work_place_address"],
            job_ad_json["cvr"],
            job_ad_json["title"],
            job_ad_json["description"],
            job_ad_json["application_deadline"],
            job_ad_json["application_deadline_status"],
            job_ad_json["publication_date"]
        )

    @staticmethod
    def create_table_statement():
        return """
        CREATE TABLE job_ads(
            job_ad_id TEXT PRIMARY KEY,
            country TEXT,
            postal_code TEXT,
            postal_district_name TEXT,
            hiring_org_name TEXT,
            occupation TEXT,
            job_ad_url TEXT,
            work_place_address TEXT,
            cvr INTEGER,
            title TEXT,
            description TEXT,
            application_deadline INTEGER,
            application_deadline_status TEXT,
            publication_date INTEGER
        );
        """

    @staticmethod
    def from_dict(job_ad_dict: dict):
        return JobAd(
            country=job_ad_dict["country"],
            postal_code=job_ad_dict["postalCode"],
            postal_district_name=job_ad_dict["postalDistrictName"],
            hiring_org_name=job_ad_dict["hiringOrgName"],
            occupation=job_ad_dict["occupation"],
            job_ad_id=job_ad_dict["jobAdId"],
            job_ad_url=job_ad_dict["jobAdUrl"],
            work_place_address=job_ad_dict["workPlaceAddress"],
            cvr=job_ad_dict["cvr"],
            title=job_ad_dict["title"],
            description=job_ad_dict["description"],
            application_deadline=datetime.fromisoformat(job_ad_dict["applicationDeadline"]),
            application_deadline_status=job_ad_dict["applicationDeadlineStatus"],
            publication_date=datetime.fromisoformat(job_ad_dict["publicationDate"])
        )
