import unittest

from whitakers_words.datatypes import Inflect, Stem
from whitakers_words.matcher import _noun_checker


class NounMatcherTest(unittest.TestCase):
    def test_basic_success(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["C"])
        infl = Inflect(stem=1, n=[1, 1], form=["C"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_bad_stem(self):
        stem = Stem(stem_number=1)
        infl = Inflect(stem=1, n=[1, 1])
        self.assertFalse(_noun_checker(stem, infl))

    def test_bad_infl(self):
        stem = Stem(stem_number=1, n=[1, 1])
        infl = Inflect(stem=1)
        self.assertFalse(_noun_checker(stem, infl))

    def test_good_wildcard_infl_succeeds(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["F"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "F"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_mismatch_infl_fails(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["F"])
        infl = Inflect(stem=1, n=[2, 1], form=["NOM", "S", "F"])
        self.assertFalse(_noun_checker(stem, infl))

    def test_bad_wildcard_infl_fails(self):
        stem = Stem(stem_number=1, n=[2, 1], form=["F"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "F"])
        self.assertFalse(_noun_checker(stem, infl))

    def test_gender_succeeds_m(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["M"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "M"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_gender_succeeds_f(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["N"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "N"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_gender_succeeds_n(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["N"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "N"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_wrong_gender_fails_mf(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["M"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "F"])
        self.assertFalse(_noun_checker(stem, infl))

    def test_wrong_gender_fails_fn(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["F"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "N"])
        self.assertFalse(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_fx(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["F"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "X"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_mx(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["M"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "X"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_nx(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["N"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "X"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_succeeds_fc(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["F"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "C"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_succeeds_mc(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["M"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "C"])
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_fails_nc(self):
        stem = Stem(stem_number=1, n=[1, 1], form=["N"])
        infl = Inflect(stem=1, n=[1, 0], form=["NOM", "S", "C"])
        self.assertFalse(_noun_checker(stem, infl))
