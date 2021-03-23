import unittest

from whitakers_words.parser import Parser


class PrepositionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    # TODO write actual tests
    def test_preposition(self):
        self.par.parse("super")

    def test_de(self):
        self.par.parse("de")
