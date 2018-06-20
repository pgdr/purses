#!/usr/bin/env python
import curses
from .controller import Controller
from .model import Model


def main():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    from sys import argv
    if len(argv) != 2:
        exit('Usage: purses.py data/iris.csv')
    try:
        model = Model.load(argv[1])
        controller = Controller(model, stdscr)
        controller.loop()
    except Exception:
        raise
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
