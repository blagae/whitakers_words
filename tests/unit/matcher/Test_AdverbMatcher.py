import unittest

from whitakers_words.datatypes import Inflect, Stem
from whitakers_words.matcher import _adv_checker


class AdverbMatcherTest(unittest.TestCase):
    def test_basic_success_pos(self):
        stem = Stem(form=["POS"])
        infl = Inflect(form=["POS"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_basic_success_comp(self):
        stem = Stem(form=["COMP"])
        infl = Inflect(form=["COMP"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_basic_success_super(self):
        stem = Stem(form=["SUPER"])
        infl = Inflect(form=["SUPER"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_bad_stem(self):
        with self.assertRaises(KeyError):
            stem = Stem()
            infl = Inflect(form=["POS"])
            _adv_checker(stem, infl)

    def test_bad_infl(self):
        with self.assertRaises(KeyError):
            stem = Stem(form=["POS"])
            infl = Inflect()
            _adv_checker(stem, infl)

    def test_wildcard_pos(self):
        stem = Stem(form=["X"], stem_number=0)
        infl = Inflect(form=["POS"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_wildcard_comp(self):
        stem = Stem(form=["X"], stem_number=1)
        infl = Inflect(form=["COMP"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_wildcard_sup(self):
        stem = Stem(form=["X"], stem_number=2)
        infl = Inflect(form=["SUPER"])
        self.assertTrue(_adv_checker(stem, infl))

    def test_wildcard_comp_fail(self):
        stem = Stem(form=["X"], stem_number=2)
        infl = Inflect(form=["COMP"])
        self.assertFalse(_adv_checker(stem, infl))
