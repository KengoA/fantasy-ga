# fantasy-ga
**fantasy-ga** is a Python module and a command line tool that uses genetic algorithm to automate the generation of fantasy sports linesups. Currently supports DraftKings basketball rules.
## Installation
 - Dependency
    - Python >= 3.9
    - `numpy`
```bash
pip install fantasy-ga
```

## Usage
Provide a `numpy.ndarray` where the columns correspond to player ID, salary, fantasy points (FPTS) and position information i.e. `player_id,salary,fpts,PG,SG,SF,PF,C,G,F,Util`.

### Python
```python
import numpy as np
from fantasy_ga import LineupGenerator

m = np.loadtxt('examples/mat.csv', delimiter=',', skiprows=1)
n_pop = 1000
n_breed = 30
n_mutate = 30
n_gen = 16
n_compound = 5

model = LineupGenerator(m, n_pop, n_gen, n_breed, n_mutate, n_compound)
lineups, fit = model.compound()
optimal_lineups, top_n_scores = model.get_top_n_lineups(lineups, fit, 1)
```

### CLI

As a module
```
$ python -m fantasy_ga --filepath=examples/mat.csv --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=1
> PlayerIDs: [ 17. 106.  70.   0.  63.  33.   1. 108.], FPTS: 308.62082
```
or a command
```
$ fantasy-ga --filepath=examples/mat.csv --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=1
> PlayerIDs: [ 17. 106.  70.   0.  63.  33.   1. 108.], FPTS: 308.62082
```