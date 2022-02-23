import unittest

from whitakers_words.datatypes import Inflect, Stem
from whitakers_words.matcher import (
    Matcher,
    _adj_checker,
    _adv_checker,
    _basic_matcher,
    _dummy_false,
    _noun_checker,
    _numeral_checker,
    _pronoun_checker,
    _verb_checker,
    _vpar_checker,
)


class DummyFalseMatcher(unittest.TestCase):
    def test_unequal_wordtypes(self):
        stem = Stem(pos="N")
        infl = Inflect(pos="V")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _dummy_false)

    def test_unequal_wordtypes_verb_wrong(self):
        stem = Stem(pos="VPAR")  # doesn't exist
        infl = Inflect(pos="V")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _dummy_false)

    def test_unequal_wordtypes_verb(self):
        stem = Stem(pos="V")
        infl = Inflect(pos="VPAR")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _vpar_checker)

    def test_unequal_wordtypes_adj(self):
        stem = Stem(pos="ADJ")
        infl = Inflect(pos="ADV")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _dummy_false)

    def test_equal_wordtypes_noun(self):
        stem = Stem(pos="N")
        infl = Inflect(pos="N")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _noun_checker)

    def test_equal_wordtypes_pronoun(self):
        stem = Stem(pos="PRON")
        infl = Inflect(pos="PRON")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _pronoun_checker)

    def test_equal_wordtypes_verb(self):
        stem = Stem(pos="V")
        infl = Inflect(pos="V")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _verb_checker)

    def test_equal_wordtypes_numeral(self):
        stem = Stem(pos="NUM")
        infl = Inflect(pos="NUM")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _numeral_checker)

    def test_equal_wordtypes_adjective(self):
        stem = Stem(pos="ADJ")
        infl = Inflect(pos="ADJ")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _adj_checker)

    def test_equal_wordtypes_adverb(self):
        stem = Stem(pos="ADV")
        infl = Inflect(pos="ADV")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _adv_checker)

    def test_equal_wordtypes_basic(self):
        stem = Stem(pos="INTERR")
        infl = Inflect(pos="INTERR")
        matcher = Matcher(stem, infl)
        self.assertEqual(matcher.function, _basic_matcher)
