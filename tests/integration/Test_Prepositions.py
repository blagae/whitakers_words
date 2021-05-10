import unittest

from whitakers_words.enums import Degree, WordType
from whitakers_words.parser import Parser


class PrepositionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_preposition(self):
        result = self.par.parse("super")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 3)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], 'super')
            self.assertIn(analysis.lexeme.wordType, [WordType.PREP, WordType.ADV])

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'super')
                self.assertEqual(inflection.affix, '')
                self.assertIn(inflection.wordType, [WordType.PREP, WordType.ADV])
                if inflection.wordType == WordType.ADV:
                    self.assertTrue(inflection.has_feature(Degree.POS))
                else:
                    self.assertEqual(inflection.features, {})

    def test_de(self):
        result = self.par.parse("de")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], 'de')
            self.assertEqual(analysis.lexeme.wordType, WordType.PREP)

            self.assertEqual(len(analysis.inflections), 1)
            inflection = analysis.inflections[0]
            self.assertEqual(inflection.stem, 'de')
            self.assertEqual(inflection.affix, '')
            self.assertEqual(inflection.wordType, WordType.PREP)
            self.assertEqual(inflection.features, {})
