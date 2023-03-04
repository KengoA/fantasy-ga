import numpy as np


class LineupGenerator:
    def __init__(
        self,
        m: np.array,
        n_pop: int,
        n_gen: int,
        n_breed: int,
        n_mutate: int,
        n_compound: int,
        pos_start_idx=3,
        sal_cap=50000,
    ):
        self.m = m
        self.n_pop = n_pop
        self.n_gen = n_gen
        self.n_breed = n_breed
        self.n_mutate = n_mutate
        self.n_compound = n_compound
        self.pos_start_idx = pos_start_idx
        self.sal_cap = sal_cap
        self.lineups = []
        self.scores = []

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
            scores.append(fpts) if sal <= self.sal_cap and len(
                np.unique(lineup)
            ) == 8 else scores.append(-1)
        self.scores = np.array(scores)

    def create_random_lineups(self):
        lineups = []

        for _ in range(self.n_pop):
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

        for _ in range(self.n_breed):
            if np.array_equal(*parents):
                self.lineups = parents
                return
            else:
                breed_idx = np.random.choice(2, 8)
                new_lineups.append([parents[p, idx] for idx, p in enumerate(breed_idx)])
        self.lineups = np.vstack([parents, np.array(new_lineups)])

    def mutate(self):
        mutate_idx = np.random.choice(self.lineups.shape[0], self.n_mutate)

        for idx in mutate_idx:
            mutant = self.m[np.random.choice(self.m.shape[0]), :]
            original = self.m[
                self.m[:, 0] == np.random.choice(self.lineups[idx]).astype(int), :
            ][0]
            eligible_pos = np.where(
                mutant[self.pos_start_idx :].astype(bool)
                & original[self.pos_start_idx :].astype(bool)
            )[0]
            swap_pos = np.random.choice(eligible_pos)
            self.lineups = np.vstack([self.lineups, self.lineups[idx]])
            self.lineups[-1, swap_pos] = mutant[0]

    def evolve(self):
        for _ in range(self.n_gen):
            self.breed()
            self.mutate()
            self.calc_scores()

    def fit(self):
        self.lineups = self.create_random_lineups()
        for _ in range(self.n_compound):
            self.calc_scores()
            self.evolve()
            self.lineups = np.vstack([self.lineups, self.create_random_lineups()])
