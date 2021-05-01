import unittest

from whitakers_words.enums import Case, Gender, Number, WordType
from whitakers_words.parser import Parser


class PronounTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_pronoun(self):
        result = self.par.parse("se")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], '-')
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 2)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 's')
                self.assertEqual(inflection.affix, 'e')
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.C))
                self.assertTrue(inflection.has_feature(Number.X))

            other_features = [[x.features['Case']] for x in analysis.inflections]
            self.assertTrue([Case.ACC] in other_features)
            self.assertTrue([Case.ABL] in other_features)

    def test_personal_pronoun(self):
        result = self.par.parse("tu")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'tu')
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 2)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'tu')
                self.assertEqual(inflection.affix, '')
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.C))
                self.assertTrue(inflection.has_feature(Number.S))

            other_features = [[x.features['Case']] for x in analysis.inflections]
            self.assertTrue([Case.NOM] in other_features)
            self.assertTrue([Case.VOC] in other_features)

    def test_quos(self):
        result = self.par.parse("quos")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 5)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'qu')
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'qu')
                self.assertEqual(inflection.affix, 'os')
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.M))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Case.ACC))

    def test_tuas(self):
        result = self.par.parse("tuas")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'tu')
            self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)  # adjectival pronoun

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'tu')
                self.assertEqual(inflection.affix, 'as')
                self.assertEqual(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Gender.F))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Case.ACC))
