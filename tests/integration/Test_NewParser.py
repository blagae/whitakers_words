from whitakers_words.new_parser import NewParser
from whitakers_words.enums import Case, Degree, Gender, Mood, Number, Person, Tense, Voice, WordType

import unittest


class NewParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = NewParser()

    def test_amat(self):
        result = self.par.parse("amat")
        self.assertEquals(len(result.forms), 1)
        self.assertEquals(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEquals(analysis.lexeme.roots[0], 'am')  # wid == 2871
            self.assertEquals(analysis.lexeme.wordType, WordType.V)

            self.assertEquals(len(analysis.inflections), 1)
            expected_features = {'Mood': Mood.IND, 'Number': Number.S, 'Person': Person['3'],
                                 'Tense': Tense.PRES, 'Voice': Voice.ACTIVE}
            self.assertEquals(analysis.inflections[0].stem, 'am')
            self.assertEquals(analysis.inflections[0].affix, 'at')
            self.assertEquals(analysis.inflections[0].wordType, WordType.V)
            self.assertEquals(analysis.inflections[0].features, expected_features)

    def test_saevissimae(self):
        result = self.par.parse("saevissimae")

        self.assertEquals(len(result.forms), 1)
        self.assertEquals(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEquals(analysis.lexeme.roots[0], 'saev')  # wid == 33999
            self.assertEquals(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEquals(len(analysis.inflections), 4)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEquals(inflection.stem, 'saevissi')
                self.assertEquals(inflection.affix, 'mae')
                self.assertEquals(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Degree.SUPER))
                self.assertTrue(inflection.has_feature(Gender.F))

            other_features = [[x.features['Case'], x.features['Number']] for x in analysis.inflections]
            self.assertTrue([Case.GEN, Number.S] in other_features)
            self.assertTrue([Case.DAT, Number.S] in other_features)
            self.assertTrue([Case.VOC, Number.P] in other_features)
            self.assertTrue([Case.NOM, Number.P] in other_features)

    def test_bonorum(self):
        result = self.par.parse("bonorum")
        self.assertEquals(len(result.forms), 1)
        self.assertEquals(len(result.forms[0].analyses), 1)
        for key, analysis in result.forms[0].analyses.items():
            self.assertEquals(analysis.lexeme.roots[0], 'bon')  # wid == 6825
            self.assertEquals(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEquals(len(analysis.inflections), 2)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEquals(inflection.stem, 'bon')
                self.assertEquals(inflection.affix, 'orum')
                self.assertEquals(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Degree.POS))
                self.assertTrue(inflection.has_feature(Case.GEN))
                self.assertTrue(inflection.has_feature(Number.P))

            other_features = [x.features['Gender'] for x in analysis.inflections]
            self.assertTrue(Gender.M in other_features)
            self.assertTrue(Gender.N in other_features)
