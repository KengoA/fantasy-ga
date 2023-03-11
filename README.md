# fantasy-ga
**fantasy-ga** is a Python module and a command line tool that uses the genetic algorithm to automate the generation of fantasy sports linesups. Currently supported platforms and leagues are as follows. 


|   | NBA | NFL  | MLB  | NHL  |
|---|---|---|---|---|
| DraftKings  |  ✅  | ✅  |  ✅  |  ✅  |
| FanDuel |   |   |   |   |

## Installation
Dependencies: `numpy`
```bash
pip install fantasy-ga
```

## Usage

### Python
`LineupGenerator` class supports csv files exported from daily fantasy sports platforms for a given contest.

```python
from fantasy_ga import LineupGenerator
from fantasy_ga.configs import Site, League, ModelConfig, ContestConfig

data_path = "examples/DraftKings/NBA/DKSalaries.csv"
export_path = "examples/DraftKings/NBA/export.csv"

cc = ContestConfig(Site.DK, League.NBA)
mc = ModelConfig(
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
)

model = LineupGenerator(cc, mc)
model.read_csv(data_path)
model.fit()
# If top_n is not specified, it will save max(500, number of total lineups) lineups sorted by scores
model.export_csv(export_path, top_n=3)

lineups, scores = model.get_top_n_lineups(1)
print(
    f"""
    [Best Lineup]
    Players: {[model.id_to_name[id] for id in lineups[0]]} 
    Salary Total: {sum([model.id_to_salary[id] for id in lineups[0]])}
    Expected FPTS: {scores[0]}
    """
)
```
### Using custom `numpy.array` for player data
Alternatively, you can provide a `numpy.array` where the first 3 columns correspond to player ID, salary, fantasy points (FPTS), followed by position information. For instance, the columns correspond to `id,salary,fpts,PG,SG,SF,PF,C,G,F,UTIL` for DraftKings Fantasy Basketball. 

If you would like to use custom numpy array for data matrix instead of csv files, you can do so by using the `set_matrix()` method. For example

```Python
cc = ContestConfig(Site.DK, League.NBA)
mc = ModelConfig() # use default
m = np.array(
    [
        [0, 6600, 36.46503, 0, 0, 0, 1, 1, 0, 1, 1],
        [1, 4200, 26.760368, 0, 0, 1, 1, 0, 0, 1, 1],
        [2, 3000, 4.38538, 1, 1, 0, 0, 0, 1, 0, 1],
        [3, 5000, 27.175564, 0, 0, 0, 0, 1, 0, 0, 1],
        [4, 3400, 16.734577, 0, 1, 1, 0, 0, 1, 1, 1],
        [5, 5900, 3.4382372, 0, 1, 1, 0, 0, 1, 1, 1],
        [6, 3000, -0.18490964, 1, 1, 0, 0, 0, 1, 0, 1],
        [7, 3000, 11.075589, 0, 0, 1, 1, 0, 0, 1, 1],
        [8, 3000, 6.469783, 0, 0, 0, 0, 1, 0, 0, 1],
        [9, 3000, 8.459954, 0, 0, 0, 0, 1, 0, 0, 1],
        [10, 5700, 33.98281, 0, 0, 0, 1, 1, 0, 1, 1],
    ]
)
model = LineupGenerator(cc, mc)
model.set_matrix(m)
model.fit()
```

### Running individual steps of the Genetic Algorithm
`LineupGenerator` class has two core methods which return optimised lineups. `breed()` method chooses the best two lineups according to the sum of fantasy points with valid positions and swap players randomly (creating _children_ lineups). `mutate()` method randomly swaps players where applicable. `fit()` method wraps around those methods such that those operations are done for multiple generations with additional random lineups.

### CLI

As a Python module
```
$ python -m fantasy_ga --data_path=examples/DraftKings/NBA/DKSalaries.csv --export_path=examples/DraftKings/NBA/lineups.csv --site=DraftKings --league=NBA --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=3
```
or a CLI command
```
$ fantasy-ga --data_path=examples/DraftKings/NBA/DKSalaries.csv --export_path=examples/DraftKings/NBA/lineups.csv --site=DraftKings --league=NBA --n_pop=100 --n_gen=5 --n_breed=100 --n_mutate=100 --n_compound=10 --top_n_lineups=3
```
which generates
```
Saved top 3 lineups into "examples/DraftKings/NBA/lineups.csv".

[Best Lineup]
Players: ['Reggie Jackson', 'Max Strus', 'Anthony Edwards', "Royce O'Neale", 'Nikola Jokic', 'Dejounte Murray', 'John Collins', 'Jarrett Allen']
Salary Total: 50000
Expected FPTS: 268.13
```