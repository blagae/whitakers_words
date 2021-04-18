import unittest

from whitakers_words.enums import Case, Mood, Number, Person, Tense, Voice, WordType
from whitakers_words.parser import Parser


class VergiliusTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_arma(self):
        result = self.par.parse("arma")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for key, analysis in result.forms[0].analyses.items():
            self.assertIn(analysis.lexeme.wordType, [WordType.N, WordType.V])
            self.assertEqual(analysis.lexeme.roots[0], 'arm')

            if analysis.lexeme.wordType == WordType.N:
                self.assertEqual(len(analysis.inflections), 3)
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, 'arm')
                    self.assertEqual(inflection.affix, 'a')
                    self.assertEqual(inflection.wordType, WordType.N)
                    self.assertTrue(inflection.has_feature(Number.P))
                    # self.assertTrue(inflection.has_feature(Gender.M))
                other_features = [[x.features['Case']] for x in analysis.inflections]
                self.assertTrue([Case.NOM] in other_features)
                self.assertTrue([Case.VOC] in other_features)
                self.assertTrue([Case.ACC] in other_features)
            else:
                # self.assertEqual(len(analysis.inflections), 1)  # TODO fix VPAR
                inflection = analysis.inflections[0]
                self.assertEqual(inflection.stem, 'arm')
                self.assertEqual(inflection.affix, 'a')
                self.assertEqual(inflection.wordType, WordType.V)
                self.assertTrue(inflection.has_feature(Mood.IMP))
                self.assertTrue(inflection.has_feature(Voice.ACTIVE))
                self.assertTrue(inflection.has_feature(Tense.PRES))
                self.assertTrue(inflection.has_feature(Person["2"]))
                self.assertTrue(inflection.has_feature(Number.S))
