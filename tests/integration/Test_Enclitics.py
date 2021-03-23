import unittest

from whitakers_words.parser import Parser


class EncliticTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    # TODO write actual tests
    def test_unique(self):
        self.par.parse("quodcumque")

    def test_optional_enclitic(self):
        self.par.parse("pollice")
