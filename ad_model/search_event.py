from dataclasses import dataclass
from datetime import datetime

@dataclass
class SearchEvent:
    se_id: int
    search_terms: str
    km_radius: int
    postal_code: int
    number_of_results: int
    at_time: datetime

    @staticmethod
    def create_table_statement():
        return """
        CREATE TABLE search_events(
            se_id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_terms TEXT,
            km_radius INTEGER,
            postal_code TEXT,
            number_of_results INTEGER,
            at_time INTEGER
        );
        """


@dataclass
class SearchEventRelationJobAd:
    rel_id: int
    se_id: int
    job_ad_id: str

    @staticmethod
    def create_table_statement():
        return """
        CREATE TABLE search_event_job_ad(
            rel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            se_id INTEGER,
            job_ad_id TEXT
        );
        """
