#!/usr/bin/env python
import curses
from .controller import Controller
from .model import Model
from .view import View

def _start(df, bindings):
    stdscr = curses.initscr()
    stdscr.keypad(True)
    try:
        model = Model.load(df)
        controller = Controller(bindings, model, stdscr)
        controller.loop()
    except Exception:
        raise
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        del stdscr

def load(tabular, bindings=None):
    """Load the tabular data into curses.

       The tabular data can be a filename to a csv file or a Pandas dataframe.
       Launches a curses view.

       The `bindings` argument is optional and can be a mapping from curses keys
       (e.g., 's', '2', or 'KEY_UP') to functions with signature

           function(df, row, col) -> (handled, value)

       and if handled is True, value will be written to df[col][row].  It is
       advisable that the signature is actually

           function(df, row, col, *args, **kwargs)

       to accommodate for future changes.
    """

    if isinstance(tabular, str):
        import pandas as pd
        tabular = pd.read_csv(tabular)
    _start(tabular, bindings)

def main():
    from sys import argv
    if len(argv) != 2:
        exit('Usage: purses.py data/iris.csv')
    load(argv[1])

__version__ = '0.0.2'
