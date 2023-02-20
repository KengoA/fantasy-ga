#!/usr/bin/env python3

import numpy as np
from fantasy_ga import LineupGenerator

if __name__ == "__main__":
    # load data
    m = np.loadtxt("examples/mat.csv", delimiter=",", skiprows=1)
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
        f"[Optimal Lineup]\nPlayer IDs: {optimal_lineups[0]}\nFPTS: {top_n_scores[0]}"
    )
