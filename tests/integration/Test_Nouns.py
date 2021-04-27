import unittest

from whitakers_words.enums import Case, Gender, Number, WordType
from whitakers_words.parser import Parser


class NounTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_regionem(self):
        result = self.par.parse("regionem")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'regio')  # wid == 20451
            self.assertEqual(analysis.lexeme.wordType, WordType.N)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'region')
                self.assertEqual(inflection.affix, 'em')
                self.assertEqual(inflection.wordType, WordType.N)
                self.assertTrue(inflection.has_feature(Case.ACC))
                self.assertTrue(inflection.has_feature(Number.S))
                self.assertTrue(inflection.has_feature(Gender.C))  # TODO fix gender on nouns

    def test_templum(self):
        result = self.par.parse("templum")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'templ')  # wid == 20451
            self.assertEqual(analysis.lexeme.wordType, WordType.N)

            self.assertEqual(len(analysis.inflections), 3)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'templ')
                self.assertEqual(inflection.affix, 'um')
                self.assertEqual(inflection.wordType, WordType.N)
                self.assertTrue(inflection.has_feature(Number.S))
                # self.assertTrue(inflection.has_feature(Gender.N))  # TODO fix gender on nouns

            other_features = [[x.features['Case']] for x in analysis.inflections]
            self.assertTrue([Case.ACC] in other_features)
            self.assertTrue([Case.VOC] in other_features)
            self.assertTrue([Case.NOM] in other_features)

    def test_reginis(self):
        result = self.par.parse("reginis")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'regin')  # wid == 20451
            self.assertEqual(analysis.lexeme.wordType, WordType.N)

            self.assertEqual(len(analysis.inflections), 3)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'regin')
                self.assertEqual(inflection.affix, 'is')
                self.assertEqual(inflection.wordType, WordType.N)
                self.assertTrue(inflection.has_feature(Number.P))
                # self.assertTrue(inflection.has_feature(Gender.F))  # TODO fix gender on nouns

            other_features = [[x.features['Case']] for x in analysis.inflections]
            self.assertTrue([Case.DAT] in other_features)
            self.assertTrue([Case.ABL] in other_features)
            self.assertTrue([Case.LOC] in other_features)

    def test_temptatio_empty(self):
        result = self.par.parse("temptatio")
        # this result is empty because abacus is not a common enough word for the default parser
        # if the default is ever changed, this test will start failing, so fix the test then
        self.assertEqual(len(result.forms), 0)

    def test_peccata(self):
        result = self.par.parse("peccata")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for key, analysis in result.forms[0].analyses.items():
            self.assertIn(analysis.lexeme.wordType, [WordType.N, WordType.V])
            if analysis.lexeme.wordType == WordType.N:
                self.assertEqual(analysis.lexeme.roots[0], 'peccat')  # wid == 20451
                self.assertEqual(len(analysis.inflections), 3)
                # common properties and features
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, 'peccat')
                    self.assertEqual(inflection.affix, 'a')
                    self.assertEqual(inflection.wordType, WordType.N)
                    self.assertTrue(inflection.has_feature(Number.P))
                    # self.assertTrue(inflection.has_feature(Gender.M))  # TODO fix gender on nouns

                other_features = [[x.features['Case']] for x in analysis.inflections]
                self.assertTrue([Case.NOM] in other_features)
                self.assertTrue([Case.VOC] in other_features)
                self.assertTrue([Case.ACC] in other_features)

    def test_acer(self):
        result = self.par.parse("acer")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for key, analysis in result.forms[0].analyses.items():
            if analysis.lexeme.wordType == WordType.N:
                self.assertEqual(analysis.lexeme.roots[0], 'acer')  # wid == 3372

                self.assertEqual(len(analysis.inflections), 3)
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, 'acer')
                    self.assertEqual(inflection.affix, '')
                    self.assertEqual(inflection.wordType, WordType.N)
                    self.assertTrue(inflection.has_feature(Number.S))
                    # self.assertTrue(inflection.has_feature(Gender.N))  # TODO fix gender on nouns

                other_features = [x.features['Case'] for x in analysis.inflections]
                self.assertTrue(Case.VOC in other_features)
                self.assertTrue(Case.NOM in other_features)
                self.assertTrue(Case.ACC in other_features)
