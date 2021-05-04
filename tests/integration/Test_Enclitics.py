import unittest

from whitakers_words.enums import Case, Gender, Number, WordType
from whitakers_words.parser import Parser


class EncliticTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_unique(self):
        result = self.par.parse("quodcumque")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(result.forms[0].enclitic.text, 'cumque')
        self.assertEqual(len(result.forms[0].analyses), 4)
        for key, analysis in result.forms[0].analyses.items():
            self.assertTrue(analysis.lexeme.roots[0] == 'qu')  # wid == 6360

            # common properties and features
            for inflection in analysis.inflections:
                self.assertTrue(inflection.stem == 'qu')
                self.assertTrue(inflection.affix == 'od')

    def test_optional_enclitic(self):
        result = self.par.parse("pollice")
        self.assertEqual(len(result.forms), 1)  # cannot be analyzed as polli-ce
        self.assertIsNone(result.forms[0].enclitic)

    def test_be_ne(self):
        result = self.par.parse("bene")
        self.assertEqual(len(result.forms), 2)  # also bene
        self.assertEqual(result.forms[1].enclitic.text, 'ne')
        self.assertEqual(len(result.forms[1].analyses), 1)
        for key, analysis in result.forms[1].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'be')  # wid == 6360
            self.assertEqual(analysis.lexeme.wordType, WordType.INTERJ)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'be')
                self.assertEqual(inflection.affix, '')
                self.assertEqual(inflection.wordType, WordType.INTERJ)
                self.assertFalse(inflection.features)

    def test_cuique(self):
        result = self.par.parse("cuique")
        self.assertEqual(len(result.forms), 1)  # also bene
        self.assertEqual(result.forms[0].enclitic.text, 'que')
        # TODO self.assertEqual(len(result.forms[0].analyses), 1)

    def test_recentiave(self):
        result = self.par.parse("recentiave")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(result.forms[0].enclitic.text, 've')

    def test_regemque(self):
        result = self.par.parse("regemque")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        self.assertEqual(result.forms[0].enclitic.text, 'que')
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'rex')
            self.assertEqual(analysis.lexeme.wordType, WordType.N)

            self.assertEqual(len(analysis.inflections), 1)
            inflection = analysis.inflections[0]

            self.assertEqual(inflection.stem, 'reg')
            self.assertEqual(inflection.affix, 'em')
            self.assertEqual(inflection.wordType, WordType.N)
            self.assertTrue(inflection.has_feature(Case.ACC))
            self.assertTrue(inflection.has_feature(Number.S))
            self.assertTrue(inflection.has_feature(Gender.C))

    def test_mecum(self):
        result = self.par.parse("mecum")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        self.assertEqual(result.forms[0].enclitic.text, 'cum')
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'ego')
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 2)
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'm')
                self.assertEqual(inflection.affix, 'e')
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Number.S))
                self.assertTrue(inflection.has_feature(Gender.C))
            other_features = [[x.features['Case']] for x in analysis.inflections]
            self.assertTrue([Case.ABL] in other_features)
            self.assertTrue([Case.ACC] in other_features)  # TODO fix false positive

    def test_tertiuscum_empty(self):
        result = self.par.parse("tertiuscum")
        self.assertEqual(len(result.forms), 0)
