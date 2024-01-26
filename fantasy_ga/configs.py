"""
Configurations for Contests and Optimizer Model
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, conint


class League(Enum):
    """
    Enum for different sports leagues. Common across different platforms.

    Values
    - UNKNOWN: Unknown league
    - NBA: National Basketball Association
    - NFL: National Football League
    - MLB: Major League Baseball
    - NHL: National Hockey League
    """

    UNKNOWN = 0
    NBA = 1
    NFL = 2
    MLB = 3
    NHL = 4


class Site(Enum):
    """
    Enum for different fantasy sports platforms.

    Values
    - UNKNOWN: Unknown platform
    - DK: DraftKings
    - FD: FanDuel
    """

    UNKNOWN = 0
    DK = 1
    FD = 2


POSITIONS = {
    # https://www.draftkings.co.uk/help/rules/overview
    Site.DK: {
        League.NBA: ["PG", "SG", "SF", "PF", "C", "G", "F", "UTIL"],
        League.MLB: ["P", "P", "C", "1B", "2B", "3B", "SS", "OF", "OF", "OF"],
        League.NFL: ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "FLEX", "DST"],
        League.NHL: ["C", "C", "W", "W", "W", "D", "D", "G", "UTIL"],
    }
}

SALARY_CAPS = {
    # https://www.draftkings.co.uk/help/rules/overview
    Site.DK: {
        League.NBA: 50000,
        League.MLB: 50000,
        League.NFL: 50000,
        League.NHL: 50000,
    }
}


class ContestConfig(BaseModel):
    """
    Config for a contest, specifying the site and league.

    Attributes:
        site (Site): The site where the contest is hosted. Currently only DraftKings is supported.
        league (League): The sports league associated with the contest.
    """

    site: Site = Site.DK
    league: League = League.NBA


class ModelConfig(BaseModel):
    """
    Config for the optimizer, specifying parameters for the genetic algorithm.

    Attributes:
        n_pop (Optional[conint(ge=0)]): Size of the initial population.
        n_breed (Optional[conint(ge=0)]): Number of player pairs to breed in each generation.
        n_mutate (Optional[conint(ge=0)]): Number to players to mutate in each generation.
        n_gen (Optional[conint(ge=0)]): Number of generations.
        n_compound (Optional[conint(ge=0)]): Size of initial populations to compound over.

    Note:
        All parameters are optional and have default values if not specified.
    """

    n_pop: Optional[conint(ge=0)] = 1000
    n_breed: Optional[conint(ge=0)] = 30
    n_mutate: Optional[conint(ge=0)] = 30
    n_gen: Optional[conint(ge=0)] = 16
    n_compound: Optional[conint(ge=0)] = 5
