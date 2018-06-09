from open_words.parse import Parse

import unittest
import json


class CrashTest(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self.par = Parse()

    def parse(self, word):
        return self.par.parse(word)

    def test_unique(self):
        val = self.parse("quodcumque")
        print(json.dumps(val, indent=2))

    def test_regular(self):
        val = self.parse("cecidit")
        print(json.dumps(val, indent=2))
