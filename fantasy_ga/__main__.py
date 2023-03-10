import argparse
from fantasy_ga.lineup_generator import LineupGenerator
from fantasy_ga.configs import Site, League, ModelConfig, ContestConfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        help="File path to the csv file exported from daily fantasy platforms",
    )
    parser.add_argument(
        "--export_path",
        help="File path to export the top lineups",
    )
    parser.add_argument("--site", help="Site name. Currently supports DraftKings/DK")
    parser.add_argument("--league", help="League name. Currently supports NBA")
    parser.add_argument("--top_n_lineups", help="top N lineups to display")
    parser.add_argument("--n_pop", help="Number of initial population to sample from")
    parser.add_argument("--n_gen", help="Number of generations to run evolution cycles")
    parser.add_argument("--n_breed", help="Number of children lineups to generate")
    parser.add_argument("--n_mutate", help="Number of mutations for lineups")
    parser.add_argument("--n_compound", help="Number of compound evolution cycles")

    args = parser.parse_args()

    cc = ContestConfig(
        Site.DK if args.site.lower() in ["dk", "draftkings"] else Site.UNKNOWN,
        League.NBA if args.league.lower() == "nba" else League.UNKNOWN,
    )
    mc = ModelConfig(
        n_pop=int(args.n_pop),
        n_gen=int(args.n_gen),
        n_breed=int(args.n_breed),
        n_mutate=int(args.n_mutate),
        n_compound=int(args.n_compound),
    )

    model = LineupGenerator(cc, mc)
    model.read_csv(args.data_path)
    model.fit()
    model.export_csv(args.export_path, top_n=int(args.top_n_lineups))
    print(f"Top {args.top_n_lineups} lineups exported into {args.export_path}")

    lineups, scores = model.get_top_n_lineups(1)
    print(
        f"[Best Lineup]\nPlayers: {[model.id_to_name[id] for id in lineups[0]]}\nSalary Total: {sum([model.id_to_salary[id] for id in lineups[0]])}\nExpected FPTS: {scores[0]}"
    )


if __name__ == "__main__":
    main()
