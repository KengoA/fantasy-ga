# fantasy-ga
**fantasy-ga** is a Python module and a command line tool that uses genetic algorithm to automate the generation of fantasy sports linesups. Currently supports DraftKings basketball rules.
## Installation
 - Dependency
    - `numpy`
```bash
pip install fantasy-ga
```

## Usage

Export a csv file from your daily fantasy basketball platform for a given contest, and read the file with `fantasy_ga.read_csv`. Currently DraftKings is supported.

Alternatively, you can provide a `numpy.array` where the columns correspond to player ID, salary, fantasy points (FPTS) and position information i.e. `id,salary,fpts,PG,SG,SF,PF,C,G,F,UTIL`.

### Python
```python
import numpy as np
from fantasy_ga import LineupGenerator, read_csv

# load data from DraftKings salary csv
id_to_name, m = read_csv("examples/DraftKings/DKSalaries.csv", site="DraftKings")

# initial population of random lineups
n_pop = 1000
# number of evolutions to itererate breeding and mutation for
n_gen = 16
# number of children lineups to choose from two best lineups
n_breed = 30
# number of random mutations for each evolution
n_mutate = 30
# number of compound evolutions with additional random lineups
n_compound = 5

model = LineupGenerator(m, n_pop, n_gen, n_breed, n_mutate, n_compound)
lineups, scores = model.fit()
optimal_lineups, top_n_scores = model.get_top_n_lineups(lineups, scores, 1)
```

### CLI

As a module
```
$ python -m fantasy_ga --filepath=examples/DraftKings/DKSalaries.csv --site=DraftKings --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=1
> PlayerIDs: [ 17. 106.  70.   0.  63.  33.   1. 108.], FPTS: 308.62082
```
or a command
```
$ fantasy-ga --filepath=examples/DraftKings/DKSalaries.csv --site=DraftKings --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=1
> PlayerIDs: [ 17. 106.  70.   0.  63.  33.   1. 108.], FPTS: 308.62082
```