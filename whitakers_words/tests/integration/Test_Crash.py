from whitakers_words.parse import Parser

import unittest


class CrashTest(unittest.TestCase):
    """
    A test class that makes sure the most basic common use cases don't crash
    These tests do not verify anything, they're just meant to provid basic protection against unforeseen crashes
    """

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_unique(self):
        self.par.parse("quodcumque")

    def test_esse(self):
        self.par.parse("sum")

    def test_regular(self):
        self.par.parse("cecidit")

    def test_immutable(self):
        self.par.parse("et")

    def test_vol(self):
        self.par.parse("vult")

    def test_optional_enclitic(self):
        self.par.parse("pollice")

    def test_pronoun(self):
        self.par.parse("se")

    def test_preposition(self):
        self.par.parse("super")

    def test_personal_pronoun(self):
        self.par.parse("tu")

    def test_noun(self):
        self.par.parse("templum")

    def test_repeat(self):
        self.par.parse("habes")
        self.par.parse("habes")

    def test_regina(self):
        self.par.parse("regina")

    def test_abacus(self):
        print(self.par.parse("abacus"))

    def test_anceps(self):
        print(self.par.parse("anceps"))
