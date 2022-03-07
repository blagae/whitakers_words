import unittest
from whitakers_words.finder import find_inflection
from whitakers_words.enums import WordType


class FinderTest(unittest.TestCase):
    def test_basic_noun_us(self):
        us = find_inflection(WordType.N, [2, 1], ["NOM", "S", "M"])
        self.assertEqual("us", us)

    def test_basic_noun_a(self):
        a = find_inflection(WordType.N, [1, 1], ["NOM", "S", "F"])
        self.assertEqual("a", a)

    def test_basic_noun_ae(self):
        ae = find_inflection(WordType.N, [1, 1], ["GEN", "S", "F"])
        self.assertEqual("ae", ae)

    def test_basic_noun_empty(self):
        em = find_inflection(WordType.N, [3, 1], ["NOM", "S", "M"])
        self.assertEqual("", em)

    def test_basic_noun_em(self):
        em = find_inflection(WordType.N, [3, 1], ["ACC", "S", "M"])
        self.assertEqual("em", em)
