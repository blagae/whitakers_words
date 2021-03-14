from whitakers_words.new_parser import NewParser
from whitakers_words.parse import Parser

import unittest


class NewParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = NewParser()
        cls.opar = Parser()

    def test_amat(self):
        word = self.par.parse("amat")
        self.assertTrue(False)
