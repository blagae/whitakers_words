import unittest

from whitakers_words.matcher import _dummy_false


class DummyFalseMatcherTest(unittest.TestCase):
    def test_dummy_false(self):
        self.assertFalse(_dummy_false(None, None))
