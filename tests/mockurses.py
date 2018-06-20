class scr(object):
    def __init__(self):
        self.refresh_count = 0
        self.msgs = {}

    def refresh(self):
        self.refresh_count += 1

    def addstr(self, y, x, msg, attr=None):
        self.msgs[(y,x)] = (msg, attr)

    def get_message(self, y, x):
        return self.msgs.get((y,x), ('',None))[0]
