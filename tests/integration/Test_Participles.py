import unittest

from whitakers_words.enums import Case, Gender, Number, Tense, Voice, WordType
from whitakers_words.parser import Parser


class VerbalParticipleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_peccata(self):
        result = self.par.parse("peccata")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for analysis in result.forms[0].analyses.values():

            self.assertIn(analysis.lexeme.wordType, [WordType.N, WordType.V])
            if analysis.lexeme.wordType == WordType.V:
                self.assertEqual(analysis.lexeme.roots[0], 'pecc')
                self.assertEqual(len(analysis.inflections), 6)
                # common properties and features
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, 'peccat')
                    self.assertEqual(inflection.affix, 'a')
                    self.assertEqual(inflection.wordType, WordType.VPAR)
                    self.assertTrue(inflection.has_feature(Voice.PASSIVE))
                    self.assertTrue(inflection.has_feature(Tense.PERF))

                other_features = [[x.features['Case'], x.features['Number'], x.features['Gender']]
                                  for x in analysis.inflections]
                self.assertTrue([Case.NOM, Number.P, Gender.N] in other_features)
                self.assertTrue([Case.VOC, Number.P, Gender.N] in other_features)
                self.assertTrue([Case.ACC, Number.P, Gender.N] in other_features)
                self.assertTrue([Case.NOM, Number.S, Gender.F] in other_features)
                self.assertTrue([Case.VOC, Number.S, Gender.F] in other_features)
                self.assertTrue([Case.ABL, Number.S, Gender.F] in other_features)
