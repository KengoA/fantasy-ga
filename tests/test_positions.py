import numpy as np
from fantasy_ga import LineupGenerator


def test_positions_random_lineups():
    m = np.loadtxt("tests/test_data.csv", delimiter=",", skiprows=1)
    n_pop = 100
    n_breed = 5
    n_mutate = 5
    n_gen = 5
    n_compound = 5

    model = LineupGenerator(m, n_pop, n_gen, n_breed, n_mutate, n_compound)
    lineups = model.create_random_lineups()

    for l in lineups:
        player_ids = [int(id) for id in l]

        # test there's no overlap
        assert len(player_ids) == len(set(player_ids))

        # test they're all eligible for their position
        assert np.diag(m.take(player_ids, 0)[:, 3:]).sum() == 8
