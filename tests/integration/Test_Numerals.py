import unittest

from whitakers_words.enums import Case, Gender, Number, NumeralType, WordType
from whitakers_words.parser import Parser


class NumeralTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_tres(self):
        result = self.par.parse("tres")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'tr')  # wid == 33999
            self.assertEqual(analysis.lexeme.wordType, WordType.NUM)

            self.assertEqual(len(analysis.inflections), 3)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'tr')
                self.assertEqual(inflection.affix, 'es')
                self.assertEqual(inflection.wordType, WordType.NUM)
                self.assertTrue(inflection.has_feature(Gender.C))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(NumeralType.CARD))
            other_features = [[x.features['Case']] for x in analysis.inflections]   
            self.assertTrue([Case.NOM] in other_features)
            self.assertTrue([Case.VOC] in other_features)
            self.assertTrue([Case.ACC] in other_features)

    def test_tricesimarum(self):
        result = self.par.parse("tricesimarum")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'triginta')  # wid == 33999
            self.assertEqual(analysis.lexeme.wordType, WordType.NUM)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'tricesim')
                self.assertEqual(inflection.affix, 'arum')
                self.assertEqual(inflection.wordType, WordType.NUM)
                self.assertTrue(inflection.has_feature(Case.GEN))
                self.assertTrue(inflection.has_feature(Gender.F))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(NumeralType.ORD))
