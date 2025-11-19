from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class SearchEvent:
    se_id: int
    search_terms: str
    km_radius: int
    postal_code: int
    number_of_results: int
    at_time: datetime

    def to_db_ready(self) -> tuple[dict[str, int | None | Any], str, str]:
        def _tranform_value(v):
            if v is None: return None
            if isinstance(v, bool): return 1 if v else 0
            if isinstance(v, datetime): return int(v.timestamp() * 1000)
            return v

        row = { k: _tranform_value(v)
                for k, v in self.__dict__.items() }
        if row["se_id"] == -1:
            row.pop("se_id")

        cols = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        return row, cols, placeholders

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

    def to_db_ready(self) -> tuple[dict[str, int | None | Any], str, str]:
        def _tranform_value(v):
            if v is None: return None
            if isinstance(v, bool): return 1 if v else 0
            if isinstance(v, datetime): return int(v.timestamp() * 1000)
            return v

        row = { k: _tranform_value(v)
                for k, v in self.__dict__.items() }
        if row["rel_id"] == -1:
            row.pop("rel_id")

        cols = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        return row, cols, placeholders

    @staticmethod
    def create_table_statement():
        return """
        CREATE TABLE search_event_job_ad(
            rel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            se_id INTEGER,
            job_ad_id TEXT
        );
        """
