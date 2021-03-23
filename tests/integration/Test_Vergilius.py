import unittest

from whitakers_words.parser import Parser


class VergiliusTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_arma(self):
        word = self.par.parse("arma")
        print(word)

    def test_regis(self):
        word = self.par.parse("regis")
        print(word)
