import unittest

from whitakers_words.enums import Case, Gender, Mood, Number, Person, PronounType, Tense, Voice, WordType
from whitakers_words.parser import Parser, UniqueInflection, UniqueLexeme


class UniquesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_quidquid(self):
        result = self.par.parse("quidquid")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        analysis = result.forms[0].analyses[0]
        self.assertIsInstance(analysis.lexeme, UniqueLexeme)
        self.assertEqual(analysis.lexeme.wordType, WordType.PRON)
        self.assertEqual(len(analysis.inflections), 2)
        for inflection in analysis.inflections:
            self.assertIsInstance(inflection, UniqueInflection)
            self.assertEqual(inflection.stem, 'quidquid')
            self.assertEqual(inflection.affix, '')
            self.assertEqual(inflection.wordType, WordType.PRON)
            self.assertTrue(inflection.has_feature(Number.S))
            self.assertTrue(inflection.has_feature(Gender.N))

        other_features = [(x.features['Case'], x.features['PronounType']) for x in analysis.inflections]
        self.assertTrue((Case.ACC, PronounType.ADJECT) in other_features)
        self.assertTrue((Case.NOM, PronounType.INDEF) in other_features)

    def test_esse(self):
        result = self.par.parse("esses")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        analysis = result.forms[0].analyses[0]
        self.assertEqual(len(analysis.inflections), 1)
        self.assertIsInstance(analysis.inflections[0], UniqueInflection)
        self.assertIsInstance(analysis.lexeme, UniqueLexeme)
        self.assertEqual(analysis.lexeme.wordType, WordType.V)
        features = {"Mood": Mood.SUB, "Number": Number.S, "Person": Person["2"],
                    "Tense": Tense.IMPF, "Voice": Voice.ACTIVE}
        self.assertEqual(analysis.inflections[0].features, features)

    def test_vol(self):
        result = self.par.parse("vult")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        analysis = result.forms[0].analyses[0]
        self.assertEqual(len(analysis.inflections), 1)
        self.assertIsInstance(analysis.inflections[0], UniqueInflection)
        self.assertIsInstance(analysis.lexeme, UniqueLexeme)
        self.assertEqual(analysis.lexeme.wordType, WordType.V)
        features = {"Mood": Mood.IND, "Number": Number.S, "Person": Person["3"],
                    "Tense": Tense.PRES, "Voice": Voice.ACTIVE}
        self.assertEqual(analysis.inflections[0].features, features)

    def test_fuerunt(self):
        """ This test is explicitly added for the source data error in esse.py
        where the tense said 'F PERF' instead of 'FUTP', as elsewhere """
        result = self.par.parse("fuerunt")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        analysis = result.forms[0].analyses[0]
        self.assertEqual(len(analysis.inflections), 2)

        for inflection in analysis.inflections:
            self.assertIsInstance(inflection, UniqueInflection)
            self.assertEqual(inflection.stem, 'fuerunt')
            self.assertEqual(inflection.affix, '')
            self.assertEqual(inflection.wordType, WordType.V)
            self.assertTrue(inflection.has_feature(Mood.IND))
            self.assertTrue(inflection.has_feature(Number.P))
            self.assertTrue(inflection.has_feature(Voice.ACTIVE))
            self.assertTrue(inflection.has_feature(Person["3"]))

        other_features = [x.features['Tense'] for x in analysis.inflections]
        self.assertTrue(Tense.FUTP in other_features)
        self.assertTrue(Tense.PERF in other_features)
