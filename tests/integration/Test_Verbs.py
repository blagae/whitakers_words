import unittest

from whitakers_words.enums import Mood, Number, Person, Tense, Voice, WordType
from whitakers_words.parser import Parser


class VerbTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_amat(self):
        result = self.par.parse("amat")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'am')  # wid == 2871
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {'Mood': Mood.IND, 'Number': Number.S, 'Person': Person['3'],
                                 'Tense': Tense.PRES, 'Voice': Voice.ACTIVE}
            self.assertEqual(analysis.inflections[0].stem, 'am')
            self.assertEqual(analysis.inflections[0].affix, 'at')
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_quaero(self):
        result = self.par.parse("quaerebar")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'quaer')  # wid == 32642
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {'Mood': Mood.IND, 'Number': Number.S, 'Person': Person['1'],
                                 'Tense': Tense.IMPF, 'Voice': Voice.PASSIVE}
            self.assertEqual(analysis.inflections[0].stem, 'quaer')
            self.assertEqual(analysis.inflections[0].affix, 'ebar')
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)
