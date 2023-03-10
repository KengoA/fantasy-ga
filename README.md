# fantasy-ga
**fantasy-ga** is a Python module and a command line tool that uses genetic algorithm to automate the generation of fantasy sports linesups. Currently supported platforms and leagues are as follows. 


|   | NBA | NFL  | MLB  | NHL  |
|---|---|---|---|---|
| DraftKings  | :white_check_mark:  | Soon | Soon  |   |
| FanDuel |   |   |   |   |

## Installation
Dependencies: `numpy`
```bash
pip install fantasy-ga
```

## Usage

Export a csv file from a daily fantasy sports platform of your choice for a given contest.

Alternatively, you can provide a `numpy.array` where the first 3 columns correspond to player ID, salary, fantasy points (FPTS), followed by position information e.g. `id,salary,fpts,PG,SG,SF,PF,C,G,F,UTIL` for basketball.

### Python
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