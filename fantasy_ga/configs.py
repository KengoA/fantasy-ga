from enum import Enum
from dataclasses import dataclass


class League(Enum):
    UNKNOWN = 0
    NBA = 1
    NFL = 2
    MLB = 3
    NHL = 4


class Site(Enum):
    UNKNOWN = 0
    DK = 1
    FD = 2


POSITIONS = {
    Site.DK: {
        League.NBA: ["PG", "SG", "SF", "PF", "C", "G", "F", "UTIL"],
        League.MLB: ["P", "P", "C", "1B", "2B", "3B", "SS", "OF", "OF", "OF"],
        League.NFL: ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "FLEX", "DST"],
        League.NHL: ["C", "C", "W", "W", "W", "D", "D", "G", "UTIL"],
    }
}

SALARY_CAPS = {
    Site.DK: {
        League.NBA: 50000,
        League.MLB: 50000,
        League.NFL: 50000,
        League.NHL: 50000,
    }
}


@dataclass
class ContestConfig:
    site: Site = Site.DK
    league: League = League.NBA


@dataclass
class ModelConfig:
    n_pop: int = 1000
    n_breed: int = 30
    n_mutate: int = 30
    n_gen: int = 16
    n_compound: int = 5
