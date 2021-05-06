import unittest

from whitakers_words.matcher import _check_right_stem


class RightStemMatcherTest(unittest.TestCase):
    def test_basic_first_stem(self):
        stem = {"orth": "test"}
        infl = {"stem": 0}
        word = {"parts": ["test"]}
        self.assertTrue(_check_right_stem(stem, infl, word))

    def test_basic_first_stem_fails_not_enough_parts(self):
        stem = {"orth": "test"}
        infl = {"stem": 1}
        word = {"parts": ["test"]}
        self.assertFalse(_check_right_stem(stem, infl, word))

    def test_basic_first_stem_fails_no_match(self):
        stem = {"orth": "test"}  # TODO maybe change check by adding stem# to stem dict instead of referring to word ?
        infl = {"stem": 0}
        word = {"parts": ["te", "test"]}
        self.assertFalse(_check_right_stem(stem, infl, word))
