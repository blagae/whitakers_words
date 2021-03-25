import unittest

from whitakers_words.enums import WordType
from whitakers_words.parser import Parser


class ConjunctionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    # TODO write actual tests
    def test_immutable(self):
        result = self.par.parse("et")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'et')  # wid == 6360
            self.assertEqual(analysis.lexeme.wordType, WordType.CONJ)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'et')
                self.assertEqual(inflection.affix, '')
                self.assertEqual(inflection.wordType, WordType.CONJ)
                self.assertFalse(inflection.features)
