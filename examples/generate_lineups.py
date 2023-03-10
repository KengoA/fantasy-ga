from fantasy_ga import LineupGenerator
from fantasy_ga.configs import Site, League, ModelConfig, ContestConfig

if __name__ == "__main__":
    data_path = "examples/DraftKings/NBA/DKSalaries.csv"
    export_path = "examples/DraftKings/NBA/lineups.csv"

    cc = ContestConfig(Site.DK, League.NBA)
    mc = ModelConfig(
        n_pop=1000,
        n_breed=30,
        n_mutate=30,
        n_gen=16,
        n_compound=5,
    )

    model = LineupGenerator(cc, mc)
    model.read_csv(data_path)
    model.fit()
    model.export_csv(export_path, top_n=3)
    print(f"Top 3 linesups exported into {export_path}")

    lineups, scores = model.get_top_n_lineups(1)
    print(
        f"[Best Lineup]\nPlayers: {[model.id_to_name[id] for id in lineups[0]]}\nSalary Total: {sum([model.id_to_salary[id] for id in lineups[0]])}\nExpected FPTS: {scores[0]}"
    )
