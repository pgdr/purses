import curses
from .view import View

class Controller(object):
    def __init__(self, model, scr):
        self._shutdown = False
        self.model = model
        self.scr = scr
        self.view = View(scr,
                         self.model.rows,
                         self.model.columns)

        def shutdown():
            self._shutdown = True

        def helptext():
            self.view.message('q for quit, DEL for delete, '
                              'UP/DOWN/RIGHT/LEFT to navigate, '
                              '0-9 to insert')

        self._controlling = {
            'q': shutdown,
            'h': helptext,
        }

        self._navigation = {
            'KEY_UP': model.up,
            'KEY_DOWN': model.down,
            'KEY_RIGHT': model.right,
            'KEY_LEFT': model.left,
            # moving view:
            'kUP5': self.view.up,
            'kDN5': self.view.down,
            'kRIT5': self.view.right,
            'kLFT5': self.view.left,
        }

        def __insert(model, i):
            return lambda: model.insert(i)

        self._editing = {
            'KEY_DC': model.delete,
        }
        self._editing.update(
            {'{}'.format(i) : __insert(model, i) for i in range(10)}
        )


    def _nav(self, key):
        if key in self._navigation:
            self._navigation[key]()
            return True
        return False

    def _editor(self, key):
        if key in self._editing:
            self._editing[key]()
            return True
        return False

    def _control(self, key):
        if key in self._controlling:
            self._controlling[key]()
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
                self.message(self.model.coords)
            elif self._editor(user):
                self.message(user)
            elif self._control(user):
                pass
            else:
                self.message('Unkown key {}'.format(user))
