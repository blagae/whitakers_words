import unittest

from whitakers_words.enums import WordType
from whitakers_words.finder import find_infl


class FinderTest(unittest.TestCase):
    def test_basic_noun_us(self):
        us = find_infl(WordType.N, [2, 1], ["NOM", "S", "M"])
        self.assertEqual("us", us)

    def test_basic_noun_a(self):
        a = find_infl(WordType.N, [1, 1], ["NOM", "S", "F"])
        self.assertEqual("a", a)

    def test_basic_noun_ae(self):
        ae = find_infl(WordType.N, [1, 1], ["GEN", "S", "F"])
        self.assertEqual("ae", ae)

    def test_basic_noun_empty(self):
        em = find_infl(WordType.N, [3, 1], ["NOM", "S", "M"])
        self.assertEqual("", em)

    def test_basic_noun_em(self):
        em = find_infl(WordType.N, [3, 1], ["ACC", "S", "M"])
        self.assertEqual("em", em)

    def test_basic_numeral_us(self):
        us = find_infl(WordType.NUM, [2, 2], ["NOM", "S", "M", "ORD"])
        self.assertEqual("us", us)

    def test_basic_numeral_a(self):
        a = find_infl(WordType.NUM, [2, 1], ["NOM", "S", "F", "ORD"])
        self.assertEqual("a", a)

    def test_basic_numeral_ae(self):
        ae = find_infl(WordType.NUM, [2, 1], ["GEN", "S", "F", "ORD"])
        self.assertEqual("ae", ae)

    def test_basic_numeral_em(self):
        um = find_infl(WordType.NUM, [2, 1], ["ACC", "S", "M", "ORD"])
        self.assertEqual("um", um)

    def test_basic_adjective_us(self):
        us = find_infl(WordType.ADJ, [1, 1], ["NOM", "S", "M", "POS"])
        self.assertEqual("us", us)

    def test_basic_adjective_a(self):
        a = find_infl(WordType.ADJ, [1, 1], ["NOM", "S", "F", "POS"])
        self.assertEqual("a", a)

    def test_basic_adjective_ae(self):
        ae = find_infl(WordType.ADJ, [1, 1], ["GEN", "S", "F", "POS"])
        self.assertEqual("ae", ae)

    def test_basic_adjective_empty(self):
        em = find_infl(WordType.ADJ, [3, 1], ["NOM", "S", "M", "POS"])
        self.assertEqual("", em)

    def test_basic_adjective_em(self):
        em = find_infl(WordType.ADJ, [3, 1], ["ACC", "S", "M", "POS"])
        self.assertEqual("em", em)

    def test_basic_verb_em(self):
        em = find_infl(WordType.V, [1, 1], ["PRES", "ACTIVE", "SUB", "1", "S"])
        self.assertEqual("em", em)

    def test_basic_verb_mini(self):
        i = find_infl(WordType.V, [3, 1], ["PRES", "PASSIVE", "IND", "2", "P"])
        self.assertEqual("imini", i)

    def test_basic_verb_i(self):
        i = find_infl(WordType.V, [3, 1], ["PERF", "ACTIVE", "IND", "1", "S"])
        self.assertEqual("i", i)

    def test_basic_verb_are(self):
        are = find_infl(WordType.V, [1, 1], ["PRES", "ACTIVE", "INF", "0", "X"])
        self.assertEqual("are", are)

    def test_basic_verb_isse(self):
        isse = find_infl(WordType.V, [1, 1], ["PERF", "ACTIVE", "INF", "0", "X"])
        self.assertEqual("isse", isse)

    def test_basic_verbal_participle_us(self):
        us = find_infl(WordType.VPAR, [3, 1], ["NOM", "S", "M", "PERF", "PASSIVE"])
        self.assertEqual("us", us)
