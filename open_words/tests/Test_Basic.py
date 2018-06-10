from open_words.parse import Parse

import unittest
import json


class CrashTest(unittest.TestCase):

    def __init__(self, meth):
        super().__init__(meth)
        self.par = Parse()

    def parse(self, word):
        print(self.par.parse(word))

    def test_unique(self):
        self.parse("quodcumque")

    def test_regular(self):
        self.parse("cecidit")

    def test_immutable(self):
        self.parse("et")
