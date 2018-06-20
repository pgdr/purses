import curses

CELL_WIDTH = 2 + 1 + 3 # 12.123
PADDING = 3 # to accomodate ' | '

class View(object):

    def __init__(self, scr, rows, cols):
        self.scr = scr
        self._top = self._left = 0
        self.pad = curses.newpad(rows, cols*(CELL_WIDTH + PADDING))

    def up(self):
        self._top = max(0, self._top - 1)
    def down(self):
        self._top += 1
    def left(self):
        self._left = max(0, self._left - 1)
    def right(self):
        self._left += 1

    def message(self, msg):
        if not isinstance(msg, str):
            msg = '{} [{}]'.format(msg, type(msg))
        self.scr.addstr(0, 0, msg, curses.A_BOLD)
        self.scr.refresh()

    def draw(self, model):
        rows, cols = model.rows, model.columns
        for y in range(self._top, self._top + 10):
            for x in range(self._left, self._left + 5):
                entry = model.cell(y, x)
                entry = entry[:max(len(entry), CELL_WIDTH)]
                try:
                    if (y,x) == model.coords:
                        self.pad.addstr(y, (x*(CELL_WIDTH+PADDING)), entry, curses.A_UNDERLINE)
                    else:
                        self.pad.addstr(y, (x*(CELL_WIDTH+PADDING)), entry)
                except curses.error:
                    pass

        # 0,0 is topleft cell
        self.pad.refresh(self._top,self._left, self._top+5,self._left+5, 20,75)
