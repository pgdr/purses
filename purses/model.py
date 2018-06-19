import pandas as pd

class Model(object):
    def __init__(self, df):
        self.df = df
        self.row = 0
        self.col = 0

    @staticmethod
    def load(fname):
        return Model(pd.read_csv(fname))

    @property
    def coords(self):
        return self.row, self.col

    @property
    def rows(self):
        return len(self.df)
    @property
    def columns(self):
        return len(self.df.columns)

    def _assert_index(self, y, x):
        assert 0 <= y < self.rows, '0 <= {} < {}'.format(y, self.rows)
        assert 0 <= x < self.columns, '0 <= {} < {}'.format(x, self.columns)

    def up(self):
        self.row = max(0, self.row - 1)
    def down(self):
        self.row += 1
    def left(self):
        self.col = max(0, self.col - 1)
    def right(self):
        self.col += 1

    def delete(self):
        self.df.iat[self.row, self.col] = 0.

    def cell(self, y=None, x=None):
        if y is None:
            y = self.row
        if x is None:
            x = self.col
        self._assert_index(y, x)
        r = list(self.df.iloc[y])
        cell = str(r[x])
        return cell
