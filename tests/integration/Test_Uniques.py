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
        self.assertEqual(len(analysis.inflections), 1)
        self.assertIsInstance(analysis.inflections[0], UniqueInflection)
        self.assertIsInstance(analysis.lexeme, UniqueLexeme)
        self.assertEqual(analysis.lexeme.wordType, WordType.PRON)
        # TODO also NOM
        features = {"Case": Case.ACC, "Number": Number.S, "Gender": Gender.N, "PronounType": PronounType.ADJECT}
        self.assertEqual(analysis.inflections[0].features, features)

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
