import numpy as np
from fantasy_ga import LineupGenerator
from fantasy_ga.configs import ModelConfig, ContestConfig, Site, League


def test_positions_random_lineups():
    cc = ContestConfig(site=Site.DK, league=League.NBA)
    mc = ModelConfig()

    model = LineupGenerator(cc, mc)
    model.set_matrix(np.loadtxt("tests/test_data.csv", delimiter=",", skiprows=1))
    lineups = model.create_random_lineups()

    for l in lineups:
        player_ids = [int(id) for id in l]

        # test there's no overlap
        assert len(player_ids) == len(set(player_ids))

        # test they're all eligible for their position
        assert np.diag(model.m.take(player_ids, 0)[:, 3:]).sum() == len(
            model._positions
        )
