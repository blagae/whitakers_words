from open_words.parse import Parser

import unittest
import json


class CrashTest(unittest.TestCase):
    """
    A test class that makes sure the most basic common use cases don't crash
    These tests do not verify anything, they're just meant to provid basic protection against unforeseen crashes
    """

    def __init__(self, meth):
        super().__init__(meth)
        self.par = Parser()

    def parse(self, word):
        print(json.dumps(self.par.parse(word), indent=2))

    def test_unique(self):
        self.parse("quodcumque")

    def test_esse(self):
        self.parse("sum")

    def test_regular(self):
        self.parse("cecidit")

    def test_immutable(self):
        self.parse("et")

    def test_vol(self):
        self.parse("vult")

    def test_optional_enclitic(self):
        self.parse("pollice")

    def test_pronoun(self):
        self.parse("se")

    def test_preposition(self):
        self.parse("super")

    def test_personal_pronoun(self):
        self.parse("tu")

    def test_noun(self):
        self.parse("templum")

    def test_repeat(self):
        self.parse("habes")
        self.parse("habes")

    def test_regina(self):
        self.parse("regina")
