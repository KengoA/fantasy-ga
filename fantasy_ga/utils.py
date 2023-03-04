import csv
import numpy as np
from fantasy_ga.constants import DK_POSITIONS


def encode_position(s: str) -> list[int]:
    res = [0] * len(DK_POSITIONS)
    for pos in s.split("/"):
        for i in range(len(DK_POSITIONS)):
            if pos == DK_POSITIONS[i]:
                res[i] = 1
                break
    return res


def read_csv(filepath: str, site: str) -> tuple[dict, list]:
    with open(filepath, mode="r") as f:
        reader = csv.reader(f)
        _ = next(reader)
        players = []
        id_to_name = {}
        id_to_salary = {}
        if site == "DraftKings":
            for row in reader:
                id_to_name[int(row[3])] = row[2]
                id_to_salary[int(row[3])] = int(row[5])
                players.append(
                    [int(row[3]), int((row[5])), float(row[8])]
                    + encode_position(row[4])
                )
        elif site == "FanDuel":
            raise NotImplementedError
    return id_to_name, id_to_salary, np.array(players)
