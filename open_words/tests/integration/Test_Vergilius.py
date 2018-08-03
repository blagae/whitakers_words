from open_words.parse import Parser

import unittest


class VergiliusTest(unittest.TestCase):
    """
    A test class that makes sure the most basic common use cases don't crash
    These tests do not verify anything, they're just meant to provid basic protection against unforeseen crashes
    """

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_arma(self):
        word = self.par.parse("arma")
        print(word)
