import unittest
from whitakers_words.finder import find_inflection
from whitakers_words.enums import WordType

class FinderTest(unittest.TestCase):
    def test_basic(self):
        us = find_inflection(WordType.N, [2, 1], ["NOM", "S", "M"])
        self.assertEqual("us", us)
