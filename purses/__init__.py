#!/usr/bin/env python
import curses
from .controller import Controller
from .model import Model
from .view import View

class clipboard:
    def __init__(self):
        self.val = float('nan')
    def copy(self, df, row, col, nav, msg, *args, **kwargs):
        self.val = df.iat[row,col]
        msg('copied {}'.format(self.val))
    def paste(self, df, row, col, nav, msg, *args, **kwargs):
        df.iat[row, col] = self.val
        msg('paste {}'.format(self.val))
    def cut(self, df, row, col, nav, msg, *args, **kwargs):
        self.copy(df, row, col, nav, msg, *args, **kwargs)
        df.iat[row, col] = float('nan')
        msg('cut {}'.format(self.val))

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

           function(df, row, col, nav, msg) -> df / None

       and if the return value is a dataframe, that will be the new dataframe.
       It is also possible to inplace manipulate df.  It is advisable that the
       signature is actually

           function(df, row, col, nav, msg, *args, **kwargs)

       to accommodate for future changes.

       The object `nav` has 9 functions: up, down, right, left, panup, pandown,
       panright, panleft, and to.  The function to(row, col) puts curser in
       given coord.

    """

    if bindings is None:
        cp = clipboard()
        bindings = {'c': cp.copy, 'v': cp.paste, 'x': cp.cut }

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
