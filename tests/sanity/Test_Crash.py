import unittest

from whitakers_words.parser import Parser


class SanityTest(unittest.TestCase):
    """
    A test class that makes sure that the parser is not mutated
    """

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_repeat(self):
        self.par.parse("habes")
        self.par.parse("habes")
