import unittest

from whitakers_words.matcher import _basic_matcher


class BasicMatcherTest(unittest.TestCase):
    def test_basic_no_n(self):
        stem = {"n": []}
        self.assertTrue(_basic_matcher(stem, None))

    def test_basic_identical(self):
        stem = {"n": [1, 2]}
        infl = {"n": [1, 2]}
        self.assertTrue(_basic_matcher(stem, infl))

    def test_basic_non_identical(self):
        stem = {"n": [1, 2]}
        infl = {"n": [1, 3]}
        self.assertFalse(_basic_matcher(stem, infl))

    def test_basic_non_identical2(self):
        stem = {"n": [1, 2]}
        infl = {"n": [2, 2]}
        self.assertFalse(_basic_matcher(stem, infl))

    def test_basic_non_identical3(self):
        stem = {"n": [1, 2]}
        infl = {"n": [2, 3]}
        self.assertFalse(_basic_matcher(stem, infl))

    def test_basic_wildcard(self):
        stem = {"n": [1, 2]}
        infl = {"n": [1, 0]}
        self.assertTrue(_basic_matcher(stem, infl))

    def test_basic_wrong_wildcard(self):
        stem = {"n": [2, 1]}
        infl = {"n": [1, 0]}
        self.assertFalse(_basic_matcher(stem, infl))

    def test_basic_hyper_wildcard(self):
        stem = {"n": [1, 2]}
        infl = {"n": [0, 0]}
        self.assertTrue(_basic_matcher(stem, infl))
