from dataclasses import dataclass


@dataclass
class TimeSerie:
    target: str
    datapoints: list[list[float|int]]
    tags: dict[str:str]
    unit: str



