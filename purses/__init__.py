#!/usr/bin/env python
import curses
from .model import Model
from .view import message, draw, CELL_WIDTH, PADDING


def _nav(model, key):
    fn = {
        'KEY_UP': model.up,
        'KEY_DOWN': model.down,
        'KEY_RIGHT': model.right,
        'KEY_LEFT': model.left,
        }
    if fn.get(key):
        fn.get(key)()
        return True
    return False

def _editor(model, key):
    if key == 'KEY_DC':  # delete
        model.delete()
        return True
    return False

def _control(model, key):
    if key == 'h':
        return 'q for quit, DEL for delete, UP/DOWN/RIGHT/LEFT to navigate'
    return False

def loop(model, scr, pad):
    user = ''
    while user != 'q':
        draw(pad, model)
        user = scr.getkey()
        message(scr, ' '*100)
        if _nav(model, user):
            message(scr, model.coords)
        elif _editor(model, user):
            message(scr, user)
        elif _control(model, user):
            message(scr, _control(model, user))
        else:
            message(scr, 'Unkown key {}'.format(user))

def main():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    from sys import argv
    if len(argv) != 2:
        exit('Usage: purses.py data/iris.csv')
    try:
        model = Model.load(argv[1])
        pad = curses.newpad(model.rows,
                            model.columns*(CELL_WIDTH + PADDING))
        loop(model, stdscr, pad)
    except Exception as err:
        raise err
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
