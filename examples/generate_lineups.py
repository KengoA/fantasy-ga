#!/usr/bin/env python3

import numpy as np
from fantasy_ga import LineupGenerator, read_csv

if __name__ == "__main__":
    # load data from DraftKings salary csv
    id_to_name, players = read_csv("examples/DraftKings/DKSalaries.csv", site="DraftKings")
    m = np.array(players)
    n_pop = 1000
    n_breed = 30
    n_mutate = 30
    n_gen = 16
    n_compound = 5
    pos_start_idx = 3

    model = LineupGenerator(m, n_pop, n_gen, n_breed, n_mutate, n_compound)
    lineups, fit = model.compound()
    optimal_lineups, top_n_scores = model.get_top_n_lineups(lineups, fit, 1)

    print(
        f"[Optimal Lineup]\nPlayers: {[id_to_name[id] for id in optimal_lineups[0]]}\nFPTS: {top_n_scores[0]}"
    )
