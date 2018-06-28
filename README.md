# Purses

Purses is a Pandas Curses program.

It allows you to jump into a curses view of any dataframe and edit the contents,
as well as open a Pandas dataframe from the command line with the purses command
line tool.

## Installation

Either run

* `pip install purses`
* `pip install git+https://github.com/pgdr/purses`
* or clone this repository to unlock new loot boxes

## Starting Purses

Purses can be used either as a terminal tool by running `purses myfile.csv`, or
from inside a Python shell.

```python
import purses
purses.load('myfile.csv')
```

You can also load a dataframe directly

```python
import purses
import pandas as pd
df = pd.read_csv('myfile.csv')
purses.load(df)
```

## Usage

Navigation in Purses is done via the `<UP>`/`<DOWN>`/`<RIGHT>`/`<LEFT>` keys.

Quit Purses with `q`.
