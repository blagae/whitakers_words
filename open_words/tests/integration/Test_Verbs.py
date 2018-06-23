from open_words.parse import Parser

import unittest
import json


class VerbTest(unittest.TestCase):

    def __init__(self, meth):
        super().__init__(meth)
        self.par = Parser()

    def parse(self, word):
        return self.par.parse(word)

    def test_sum(self):
        result = self.parse("sum")
        print(json.dumps(result, indent=2))
