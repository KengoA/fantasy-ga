import pytest
from fantasy_ga.configs import ContestConfig, ModelConfig, Site, League


# Normal cases for ContestConfig
def test_contest_config_default_values():
    config = ContestConfig()
    assert config.site == Site.DK
    assert config.league == League.NBA


def test_contest_config_custom_values():
    config = ContestConfig(site=Site.FD, league=League.NFL)
    assert config.site == Site.FD
    assert config.league == League.NFL


# Failure cases for ContestConfig
def test_contest_config_invalid_site():
    with pytest.raises(ValueError):
        ContestConfig(site="invalid_site", league=League.NBA)


def test_contest_config_invalid_league():
    with pytest.raises(ValueError):
        ContestConfig(site=Site.DK, league="invalid_league")


# Normal cases for ModelConfig
def test_model_config_default_values():
    config = ModelConfig()
    assert config.n_pop == 1000
    assert config.n_breed == 30
    assert config.n_mutate == 30
    assert config.n_gen == 16
    assert config.n_compound == 5


def test_model_config_custom_values():
    config = ModelConfig(n_pop=500, n_breed=20, n_mutate=20, n_gen=8, n_compound=3)
    assert config.n_pop == 500
    assert config.n_breed == 20
    assert config.n_mutate == 20
    assert config.n_gen == 8
    assert config.n_compound == 3


# Failure cases for ModelConfig
def test_model_config_negative_values():
    with pytest.raises(ValueError):
        ModelConfig(n_pop=-1, n_breed=-1, n_mutate=-1, n_gen=-1, n_compound=-1)


def test_model_config_non_integer_values():
    with pytest.raises(ValueError):
        ModelConfig(
            n_pop=1,
            n_breed=[1],
            n_mutate=3,
            n_gen=4,
            n_compound=5,
        )
