import curses
from .view import View

class _navigator:
    def __init__(self, view):
        self.view = view

    def up(self):
        self.view.moveup()
    def down(self):
        self.view.movedown()
    def left(self):
        self.view.moveleft()
    def right(self):
        self.view.moveright()

    def panup(self):
        self.view.panup()
    def pandown(self):
        self.view.pandown()
    def panleft(self):
        self.view.panleft()
    def panright(self):
        self.view.panright()

    def to(self, row, col):
        self.view.to(row, col)

class _messenger:
    def __init__(self, view):
        self.view = view
    def __call__(self, message):
        self.view.message(message)



class Controller(object):
    def __init__(self, bindings, model, scr):
        self._shutdown = False
        self.model = model
        self.scr = scr
        height, width = scr.getmaxyx()
        self.view = View(scr,
                         min(height-2, self.model.rows),
                         min(width-5, self.model.columns+1)) # +1 due to index col
        self.navigator = _navigator(self.view)
        self.messenger = _messenger(self.view)

        self.__init_bindings(bindings)
        self.helptext()


    def __init_bindings(self, bindings):
        def __insert(val):
            def __f(df, row, col, *args, **kwargs):
                df.iat[row, col] = val
            return __f

        def __delete(df, row, col, *args, **kwargs):
            return __insert(float('nan'))(df, row, col)

        self._bindings = {
            # control
            'q': self.shutdown,
            'h': self.helptext,
            # navigate
            'KEY_UP': self.moveup,
            'KEY_DOWN': self.movedown,
            'KEY_RIGHT': self.moveright,
            'KEY_LEFT': self.moveleft,

            'kUP5': self.panup,
            'kDN5': self.pandown,
            'kRIT5': self.panright,
            'kLFT5': self.panleft,
            #
            'KEY_DC': __delete,
        }
        self._bindings.update(
            {'{}'.format(i) : __insert(i) for i in range(10)}
        )
        self._bindings.update(bindings)


    def shutdown(self, *args, **kwargs):  # ignore all args
        self._shutdown = True

    def helptext(self, *args, **kwargs):
        self.messenger('q for quit, DEL for delete, '
                       'UP/DOWN/RIGHT/LEFT to navigate, '
                       '0-9 to insert')

    def moveup(self, *args, **kwargs):
        self.navigator.up()
    def movedown(self, *args, **kwargs):
        self.navigator.down()
    def moveleft(self, *args, **kwargs):
        self.navigator.left()
    def moveright(self, *args, **kwargs):
        self.navigator.right()

    def panup(self, *args, **kwargs):
        self.navigator.up()
    def pandown(self, *args, **kwargs):
        self.navigator.down()
    def panleft(self, *args, **kwargs):
        self.navigator.left()
    def panright(self, *args, **kwargs):
        self.navigator.right()

    def loop(self):
        while not self._shutdown:
            self.view.draw(self.model)

            callback_args = (self.model.df,
                             self.view.coords[0], # row
                             self.view.coords[1], # col
                             self.navigator,
                             self.messenger,
                             )

            user = self.scr.getkey()
            self.messenger(' '*100)  # clears previous message
            if user in self._bindings:
                res = self._bindings[user](*callback_args)
                if res is not None:
                    self.model.df = res
            else:
                self.messenger('Unkown key {}'.format(user))
