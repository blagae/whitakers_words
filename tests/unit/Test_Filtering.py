import unittest

from whitakers_words.parser import Parser


class DataLayerTest(unittest.TestCase):
    def test_subsetting_interference(self):
        subsetParser = Parser()
        fullParser = Parser(frequency="X")
        self.assertNotEqual(len(subsetParser.data.stems), len(fullParser.data.stems))

    def test_subsetting_interference_reverse(self):
        fullParser = Parser(frequency="X")
        subsetParser = Parser()
        self.assertNotEqual(len(subsetParser.data.stems), len(fullParser.data.stems))
