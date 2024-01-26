import pytest
import os
from fantasy_ga.lineup_generator import LineupGenerator
from fantasy_ga.configs import Site, League, ModelConfig, ContestConfig

@pytest.fixture
def sample_data_path(tmpdir):
    return "examples/DraftKings/NBA/DKSalaries.csv"

@pytest.fixture
def export_path(tmpdir):
    return str(tmpdir.join("output.csv"))

def test_lineup_generator(sample_data_path, export_path):
    args = {
        "data_path": sample_data_path,
        "export_path": export_path,
        "site": "DK",
        "league": "NBA",
        "top_n_lineups": "1",
        "n_pop": "100",
        "n_gen": "20",
        "n_breed": "10",
        "n_mutate": "5",
        "n_compound": "5",
    }

    cc = ContestConfig(site=Site.DK, league=League.NBA)
    mc = ModelConfig(
        n_pop=int(args["n_pop"]),
        n_gen=int(args["n_gen"]),
        n_breed=int(args["n_breed"]),
        n_mutate=int(args["n_mutate"]),
        n_compound=int(args["n_compound"]),
    )

    model = LineupGenerator(cc, mc)
    model.read_csv(args["data_path"])
    model.fit()
    model.export_csv(args["export_path"], top_n=int(args["top_n_lineups"]))

    assert os.path.exists(args["data_path"])
    assert os.path.exists(args["export_path"])

    lineups, scores = model.get_top_n_lineups(1)
    assert len(lineups) == 1
    assert scores[0] >= 0

