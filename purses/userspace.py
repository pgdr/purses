import curses

class clipboard:
    def __init__(self):
        self.val = float('nan')

    def copy(self, model, nav, io, *args, **kwargs):
        self.val = model.get(nav.row, nav.col)
        io.message('copied {}'.format(self.val))

    def paste(self, model, nav, io, *args, **kwargs):
        model.set(self.val)
        io.message('paste {}'.format(self.val))

    def cut(self, model, nav, io, *args, **kwargs):
        self.copy(model, nav, io, *args, **kwargs)
        model.set(float('nan'))
        io.message('cut {}'.format(self.val))


def printer(model, nav, io, *args, **kwargs):
    r,c = model.cursor
    if c >= 0:
        msg = '{}: {}'.format(cursor, getter(r,c))
    else:
        msg = '{}: (at index)'.format((r,c+1))
    print(msg)

def square(model, nav, io, *args, **kwargs):
    val = model.get()
    model.set(val**2)

def deleter(model, nav, io, *args, **kwargs):
    model.set(float('inf'))


def cell_input(model, nav, io, *args, **kwargs):
    #inpt = io.user_input('Enter value to input: ')
    #try:
    #    inpt = float(inpt)
    #    df.iat[nav.row, nav.col] = inpt
    #except ValueError as err:
    #    io.message(err)
    pass

def search(model, nav, io, *args, **kwargs):
    inpt = io.user_input('Search: ')
    inpt = 5.0
    srch = str(inpt).strip()
    for r in range(model.rows):
        for c in range(model.cols):
            val = str(model.get(r,c)).strip()
            if val == srch:
                print(r, c)
                return
    io.message('Did not find {srch}'.format(srch=srch))

class summer:
    def __init__(self):
        self.sum_ = 0

    def add(self, model, nav, io, *args, **kwargs):
        self.sum_ += model.get(nav.row, nav.col)
        #io.message('Current sum: {}'.format(self.sum_))

    def flush(self, model, nav, io, *args, **kwargs):
        model.set(self.sum_)
        #io.message('Flushed: {}'.format(self.sum_))
        self.sum_ = 0


def live(M, i, j):
    def in_(coor):
        x, y = coor
        return 0 <= x < M.shape[0] and 0 <= y and y < M.shape[1]

    count = 0
    for r in range(-1, 2):
        for c in range(-1, 2):
            if c == r == 0:
                continue
            e = i + r, j + c
            if in_(e) and M[e[0]][e[1]] > 0:
                count += 1

    if M[i][j] == 1:
        return 2 <= count <= 3
    return 1 if count == 3 else 0


def game_of_life(model, nav, io, *args, **kwargs):
    import copy
    G = model.df.values
    Gp = copy.deepcopy(G)
    s = G.shape
    for i in range(s[0]):
        for j in range(s[1]):
            Gp[i][j] = live(G, i, j)
    for i in range(s[0]):
        for j in range(s[1]):
            model.set(Gp[i][j], i, j)

def default_bindings():
    autumn = summer()
    cp = clipboard()
    bindings = {'c': cp.copy, 'v': cp.paste, 'x': cp.cut,
                'i' : cell_input,
                '/' : search,
                's' : autumn.add, 'f': autumn.flush,
                'L': game_of_life,

                'p': printer,
                '2': square,
                curses.KEY_DC: deleter,
    }
    return bindings
