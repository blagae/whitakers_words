import unittest

from whitakers_words.matcher import _check_right_stem


class RightStemMatcherTest(unittest.TestCase):
    def test_basic_first_stem(self):
        stem = {"stem_number": 0}
        infl = {"stem": 0}
        self.assertTrue(_check_right_stem(stem, infl))

    def test_basic_first_stem_fails_not_enough_parts(self):
        stem = {"stem_number": 0}
        infl = {"stem": 1}
        self.assertFalse(_check_right_stem(stem, infl))

    def test_basic_first_stem_fails_no_match(self):
        stem = {"stem_number": 1}
        infl = {"stem": 0}
        self.assertFalse(_check_right_stem(stem, infl))
