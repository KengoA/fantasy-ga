import argparse
from fantasy_ga.lineup_generator import LineupGenerator
from fantasy_ga.utils import read_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        help="File path to the csv file exported from daily fantasy platforms",
    )
    parser.add_argument("--site", help="Site type. Currently supports (DraftKings)")
    parser.add_argument("--top_n_lineups", help="top N lineups to display")
    parser.add_argument("--n_pop", help="Number of initial population to sample from")
    parser.add_argument("--n_gen", help="Number of generations to run evolution cycles")
    parser.add_argument("--n_breed", help="Number of children lineups to generate")
    parser.add_argument("--n_mutate", help="Number of mutations for lineups")
    parser.add_argument("--n_compound", help="Number of compound evolution cycles")
    parser.add_argument("--sal_cap", help="Salary cap for the lineup.")

    args = parser.parse_args()

    id_to_name, id_to_salary, m = read_csv(args.filepath, args.site)
    model = LineupGenerator(
        m=m,
        n_pop=int(args.n_pop),
        n_gen=int(args.n_gen),
        n_breed=int(args.n_breed),
        n_mutate=int(args.n_mutate),
        n_compound=int(args.n_compound),
    )

    model.fit()
    lineups, scores = model.get_top_n_lineups(int(args.top_n_lineups))
    print(f"Generated Top {args.top_n_lineups} lineups")
    for lineup, score in zip(lineups, scores):
        print(
            f"\nPlayers: {[id_to_name[id] for id in lineup]}\nSalary Total: {sum([id_to_salary[id] for id in lineup])}\nExpected FPTS: {score}"
        )

if __name__ == "__main__":
    main()
