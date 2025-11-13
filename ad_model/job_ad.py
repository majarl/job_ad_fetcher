from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class JobAd:
    country: str
    postal_code: int
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