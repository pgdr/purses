#!/usr/bin/env python
import unittest

from .mockurses import scr

from purses import View

class TestView(unittest.TestCase):
    def test_message(self):
        scr_ = scr()
        view = View(scr_, 5, 10, mock=True)
        view.message('test')
        self.assertTrue(scr_.refresh_count > 0)
        self.assertEqual(scr_.get_message(0,0), 'test')

if __name__ == '__main__':
    unittest.main()
