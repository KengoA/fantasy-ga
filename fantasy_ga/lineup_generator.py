import csv
import numpy as np

from fantasy_ga.configs import (
    Site,
    ContestConfig,
    ModelConfig,
    POSITIONS,
    SALARY_CAPS,
)


class LineupGenerator:
    def __init__(
        self,
        cc: ContestConfig,
        mc: ModelConfig,
    ):
        self.m = None
        self._cc = cc
        self._mc = mc
        self._positions = POSITIONS[self._cc.site][self._cc.league]
        self._salary_cap = SALARY_CAPS[self._cc.site][self._cc.league]
        self.id_to_name = {}
        self.id_to_salary = {}
        self.lineups = []
        self.scores = []
        self.pos_start_idx = 3

    def encode_position(self, s: str) -> list[int]:
        res = [0] * len(self._positions)
        for pos in s.split("/"):
            for i in range(len(self._positions)):
                if pos == self._positions[i]:
                    res[i] = 1
                    # break if no duplicate positions allowed in the lineup
                    if len(self._positions) == len(set(self._positions)):
                        break
        return res

    def read_csv(self, filepath: str):
        with open(filepath, mode="r") as f:
            reader = csv.reader(f)
            _ = next(reader)
            players = []
            if self._cc.site == Site.DK:
                for row in reader:
                    self.id_to_name[int(row[3])] = row[2]
                    self.id_to_salary[int(row[3])] = int(row[5])
                    players.append(
                        [int(row[3]), int((row[5])), float(row[-1])]
                        + self.encode_position(row[4])
                    )
            elif self._cc.site == Site.FD:
                raise NotImplementedError
        self.m = np.array(players)

    def set_matrix(self, m: np.array):
        self.m = m

    def export_csv(self, filepath: str, top_n=None):
        n = top_n if top_n else min(500, len(self.lineups))
        lineups, _ = self.get_top_n_lineups(n)

        with open(filepath, "w") as f:
            w = csv.writer(f)
            w.writerow(self._positions)
            for lineup in lineups:
                w.writerow([_id for _id in lineup.astype(int)])

    def get_top_n_lineups(self, n):
        top_n_scores = (-self.scores).argsort()[:n]
        return self.lineups.take(top_n_scores.astype(int), 0), self.scores.take(
            top_n_scores.astype(int), 0
        )

    def calc_scores(self):
        scores = []
        for lineup in self.lineups:
            sal, fpts = self.m[np.in1d(self.m[:, 0], lineup.astype(int))][
                :, [1, 2]
            ].sum(axis=0)
            scores.append(fpts) if sal <= self._salary_cap and len(
                np.unique(lineup)
            ) == len(self._positions) else scores.append(-1)
        self.scores = np.array(scores)

    def create_random_lineups(self):
        lineups = []

        for _ in range(self._mc.n_pop):
            lineup = []
            for pos_key in range(self.pos_start_idx, self.m.shape[1]):
                candidate_ids = self.m[self.m[:, pos_key] == 1][:, 0]
                searching = True
                while searching:
                    candidate = np.random.choice(candidate_ids)
                    if candidate not in lineup:
                        lineup.append(candidate)
                        searching = False
            lineups.append(lineup)
        return np.array(lineups)

    def breed(self):
        new_lineups = []
        parents_idx = (-self.scores).argsort()[:2]
        parents = self.lineups.take(parents_idx, 0)

        for _ in range(self._mc.n_breed):
            if np.array_equal(*parents):
                self.lineups = parents
                return
            else:
                breed_idx = np.random.choice(2, len(self._positions))
                new_lineups.append([parents[p, idx] for idx, p in enumerate(breed_idx)])
        self.lineups = np.vstack([parents, np.array(new_lineups)])

    def mutate(self):
        mutate_idx = np.random.choice(self.lineups.shape[0], self._mc.n_mutate)

        for idx in mutate_idx:
            searching = True
            while searching:
                # Search for two rows where positions are swappable
                mutant = self.m[np.random.choice(self.m.shape[0]), :]
                original = self.m[
                    self.m[:, 0] == np.random.choice(self.lineups[idx]).astype(int), :
                ][0]
                eligible_pos = np.where(
                    mutant[self.pos_start_idx :].astype(bool)
                    & original[self.pos_start_idx :].astype(bool)
                )[0]
                if len(eligible_pos) > 0:
                    searching = False
            swap_pos = np.random.choice(eligible_pos)
            self.lineups = np.vstack([self.lineups, self.lineups[idx]])
            self.lineups[-1, swap_pos] = mutant[0]

    def evolve(self):
        for _ in range(self._mc.n_gen):
            self.breed()
            self.mutate()
            self.calc_scores()

    def fit(self):
        self.lineups = self.create_random_lineups()
        for _ in range(self._mc.n_compound):
            self.calc_scores()
            self.evolve()
            self.lineups = np.vstack([self.lineups, self.create_random_lineups()])
