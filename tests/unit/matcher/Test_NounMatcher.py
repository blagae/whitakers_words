import unittest

from whitakers_words.datatypes import Inflect, Stem
from whitakers_words.matcher import _noun_checker


class NounMatcherTest(unittest.TestCase):
    def test_basic_success(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="C")
        infl = Inflect(pos="N", stem=1, n=[1, 1], form="C")
        self.assertTrue(_noun_checker(stem, infl))

    def test_bad_stem(self):
        stem = Stem(pos="N", stem_number=1)
        infl = Inflect(pos="N", stem=1, n=[1, 1])
        self.assertFalse(_noun_checker(stem, infl))

    def test_bad_infl(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1])
        infl = Inflect(pos="N", stem=1)
        self.assertFalse(_noun_checker(stem, infl))

    def test_good_wildcard_infl_succeeds(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="F")
        self.assertTrue(_noun_checker(stem, infl))

    def test_mismatch_infl_fails(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[2, 1], form="F")
        self.assertFalse(_noun_checker(stem, infl))

    def test_bad_wildcard_infl_fails(self):
        stem = Stem(pos="N", stem_number=1, n=[2, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="F")
        self.assertFalse(_noun_checker(stem, infl))

    def test_gender_succeeds_m(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="M")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="M")
        self.assertTrue(_noun_checker(stem, infl))

    def test_gender_succeeds_f(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="N")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="N")
        self.assertTrue(_noun_checker(stem, infl))

    def test_gender_succeeds_n(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="N")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="N")
        self.assertTrue(_noun_checker(stem, infl))

    def test_wrong_gender_fails_mf(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="M")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="F")
        self.assertFalse(_noun_checker(stem, infl))

    def test_wrong_gender_fails_fn(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="N")
        self.assertFalse(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_fx(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="X")
        self.assertTrue(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_mx(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="M")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="X")
        self.assertTrue(_noun_checker(stem, infl))

    def test_wildcard_gender_succeeds_nx(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="N")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="X")
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_succeeds_fc(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="F")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="C")
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_succeeds_mc(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="M")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="C")
        self.assertTrue(_noun_checker(stem, infl))

    def test_common_gender_fails_nc(self):
        stem = Stem(pos="N", stem_number=1, n=[1, 1], form="N")
        infl = Inflect(pos="N", stem=1, n=[1, 0], form="C")
        self.assertFalse(_noun_checker(stem, infl))
