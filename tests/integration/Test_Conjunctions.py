import unittest

from whitakers_words.parser import Parser


class ConjunctionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    # TODO write actual tests
    def test_immutable(self):
        self.par.parse("et")
