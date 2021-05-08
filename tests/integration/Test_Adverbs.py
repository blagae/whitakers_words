import unittest

from whitakers_words.enums import Degree, WordType
from whitakers_words.parser import Parser


class AdverbTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_bene(self):
        result = self.par.parse("bene")
        self.assertEqual(len(result.forms), 2)  # also be-ne, see EncliticTest
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'bene')
            self.assertEqual(analysis.lexeme.wordType, WordType.ADV)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'bene')
                self.assertEqual(inflection.affix, '')
                self.assertEqual(inflection.wordType, WordType.ADV)
                self.assertTrue(inflection.has_feature(Degree.POS))

    def test_melius(self):
        result = self.par.parse("melius")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)  # see Test_Adjectives.test_melius
        analysis = result.forms[0].analyses[6360]
        self.assertEqual(analysis.lexeme.roots[0], 'bene')
        self.assertEqual(analysis.lexeme.wordType, WordType.ADV)

        self.assertEqual(len(analysis.inflections), 1)
        # common properties and features
        for inflection in analysis.inflections:
            self.assertEqual(inflection.stem, 'melius')
            self.assertEqual(inflection.affix, '')
            self.assertEqual(inflection.wordType, WordType.ADV)
            self.assertTrue(inflection.has_feature(Degree.COMP))
