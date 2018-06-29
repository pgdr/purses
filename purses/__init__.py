#!/usr/bin/env python
from .controller import Controller
from .model import Model
from .userspace import default_bindings


def load(tabular, bindings=None):
    """Load the tabular data into curses.

       The tabular data can be a filename to a csv file or a Pandas dataframe.
       Launches a curses view.

    """

    name = ''
    if isinstance(tabular, str):
        import pandas as pd
        name = tabular
        tabular = pd.read_csv(tabular)
    model = Model(tabular, name)
    cntrl = Controller(model)
    cntrl.add_handlers(default_bindings())
    cntrl.run()

def main():
    from sys import argv
    if len(argv) != 2:
        exit('Usage: purses.py data/iris.csv')
    load(argv[1])

if __name__ == '__main__':
    main()

__version__ = '0.0.8'
