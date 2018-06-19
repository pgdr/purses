import curses

CELL_WIDTH = 2 + 1 + 3 # 12.123
PADDING = 3 # to accomodate ' | '


def message(stdscr, msg):
    if not isinstance(msg, str):
        msg = '{} [{}]'.format(msg, type(msg))
    stdscr.addstr(0, 0, msg, curses.A_BOLD)
    stdscr.refresh()


def draw(pad, model):
    rows, cols = model.rows, model.columns
    for y in range(10):
        for x in range(5):
            entry = model.cell(y, x)
            entry = entry[:max(len(entry), CELL_WIDTH)]
            try:
                if (y,x) == model.coords:
                    pad.addstr(y, (x*(CELL_WIDTH+PADDING)), entry, curses.A_UNDERLINE)
                else:
                    pad.addstr(y, (x*(CELL_WIDTH+PADDING)), entry)
            except curses.error:
                pass

    # 0,0 is topleft cell
    pad.refresh(0,0, 5,5, 20,75)
