import curses
from .view import View

class Controller(object):
    def __init__(self, bindings, model, scr):
        self._shutdown = False
        self._bindings = bindings
        self.model = model
        self.scr = scr
        height, width = scr.getmaxyx()
        self.view = View(scr,
                         min(height-2, self.model.rows),
                         min(width-5, self.model.columns+1)) # +1 due to index col

        self._controlling = {
            'q': self.shutdown,
            'h': self.helptext,
        }

        self._navigation = {
            'KEY_UP': self.moveup,
            'KEY_DOWN': self.movedown,
            'KEY_RIGHT': self.moveright,
            'KEY_LEFT': self.moveleft,
            # moving view:
            'kUP5': self.panup,
            'kDN5': self.pandown,
            'kRIT5': self.panright,
            'kLFT5': self.panleft,
        }

        self.helptext()

        def __insert(val):
            def __f(df, row, col):
                df.iat[row, col] = val
            return __f

        def __delete(df, row, col):
            return __insert(float('nan'))(df, row, col)

        self._editing = {
            'KEY_DC': __delete,
        }
        self._editing.update(
            {'{}'.format(i) : __insert(i) for i in range(10)}
        )


    def shutdown(self, *args, **kwargs):  # ignore all args
        self._shutdown = True

    def helptext(self, *args, **kwargs):
        self.view.message('q for quit, DEL for delete, '
                          'UP/DOWN/RIGHT/LEFT to navigate, '
                          '0-9 to insert')

    def moveup(self, *args, **kwargs):
        self.view.moveup()
    def movedown(self, *args, **kwargs):
        self.view.movedown()
    def moveleft(self, *args, **kwargs):
        self.view.moveleft()
    def moveright(self, *args, **kwargs):
        self.view.moveright()

    def panup(self, *args, **kwargs):
        self.view.panup()
    def pandown(self, *args, **kwargs):
        self.view.pandown()
    def panleft(self, *args, **kwargs):
        self.view.panleft()
    def panright(self, *args, **kwargs):
        self.view.panright()


    def _nav(self, key):
        if key in self._navigation:
            self._navigation[key](self.model.df, *self.view.coords)
            return True
        return False

    def _editor(self, key):
        if key in self._editing:
            self._editing[key](self.model.df, *self.view.coords)
            return True
        return False

    def _control(self, key):
        if key in self._controlling:
            self._controlling[key](self.model.df, *self.view.coords)
            return True
        return False

    def message(self, msg):
        self.view.message(msg)

    def loop(self):
        while not self._shutdown:
            self.view.draw(self.model)
            user = self.scr.getkey()
            self.message(' '*100)  # clears previous message
            if self._nav(user):
                self.message(self.view.coords)
            elif self._editor(user):
                self.message(user)
            elif self._control(user):
                pass
            else:
                self.message('Unkown key {}'.format(user))
