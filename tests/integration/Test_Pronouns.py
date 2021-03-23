import unittest

from whitakers_words.parser import Parser


class PronounTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    # TODO write actual tests
    def test_pronoun(self):
        self.par.parse("se")

    def test_personal_pronoun(self):
        self.par.parse("tu")
