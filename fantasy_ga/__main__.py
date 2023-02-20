#!/usr/bin/env python3

import argparse
import numpy as np
from .lineup_generator import LineupGenerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", help="filepath")
    parser.add_argument("--top_n_lineups", help="filepath")
    parser.add_argument("--n_pop", help="Do the bar option")
    parser.add_argument("--n_gen", help="Foo the program")
    parser.add_argument("--n_breed", help="Foo the program")
    parser.add_argument("--n_mutate", help="Foo the program")
    parser.add_argument("--n_compound", help="Foo the program")
    parser.add_argument("--sal_cap", help="Foo the program")

    args = parser.parse_args()

    m = np.loadtxt(args.filepath, delimiter=",", skiprows=1)
    model = LineupGenerator(
        m=m,
        n_pop=int(args.n_pop),
        n_gen=int(args.n_gen),
        n_breed=int(args.n_breed),
        n_mutate=int(args.n_mutate),
        n_compound=int(args.n_compound),
    )

    lineups, fit = model.compound()
    lineups, scores = model.get_top_n_lineups(lineups, fit, int(args.top_n_lineups))
    print(f"generated top {args.top_n_lineups} lineups")
    for lineup, score in zip(lineups, scores):
        print(f"PlayerIDs: {lineup}, FPTS: {score}")


if __name__ == "__main__":
    main()
