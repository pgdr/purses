import curses

CELL_WIDTH = 2 + 1 + 3 # 12.123
PADDING = 3 # to accomodate ' | '

class View(object):

    def __init__(self, scr, rows, cols, mock=False):
        self.scr = scr
        self._top = self._left = 0
        self._row = self._col = 0  # relative index to _top and _left
        self._cols = cols
        self._rows = rows
        if not mock:
            self.pad = curses.newpad(rows, cols*(CELL_WIDTH + PADDING))

        self.col_index = scr.subwin(6, 3)
        self.header = scr.subwin(3, 10)
        self.cols = [scr.subwin(6, 8*(i+1)) for i in range(cols)]

    def moveup(self):
        self._row = max(0, self._row - 1)
    def movedown(self):
        self._row += 1
    def moveleft(self):
        self._col = max(0, self._col - 1)
    def moveright(self):
        self._col += 1

    def panup(self):
        self._top = max(0, self._top - 1)
        self.movedown()
    def pandown(self):
        self._top += 1
        self.moveup()
    def panleft(self):
        self._left = max(0, self._left - 1)
        self.moveright()
    def panright(self):
        self._left += 1
        self.moveleft()

    def message(self, msg):
        if not isinstance(msg, str):
            msg = '{} [{}]'.format(msg, type(msg))
        self.scr.addstr(0, 0, msg, curses.A_BOLD)
        self.scr.refresh()

    @property
    def coords(self):
        """Return the index in the dataframe, that is the indices + pan."""
        return self._row + self._top, self._col + self._left

    def _draw_index(self, model):
        self.col_index.clear()
        for y in range(10): # no index for top left cell
            self.col_index.addstr(y, 0, 'i={}'.format(model.df.index[y+self._top]))
        self.col_index.refresh()

    def __attr_cell(self, row, col):
        return curses.A_REVERSE if self.coords == (row, col) else curses.A_NORMAL

    def _draw_cols(self, model):
        for i in range(self._cols-1):
            self.cols[i].clear()
            for j in range(0, 10):
                entry = model.cell(j+self._top, i)
                self.cols[i].addstr(j, 0, entry, self.__attr_cell(j,i))
            self.cols[i].refresh()

    def _draw_header(self, model):
        self.header.clear()
        header = ' '.join(list(model.df.columns))  # todo add correct spacing
        self.header.addstr(0, 0, header)
        self.header.refresh()

    def draw(self, model):
        self._draw_header(model)
        self._draw_index(model)
        self._draw_cols(model)
