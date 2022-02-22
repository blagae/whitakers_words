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
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "am")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.IND,
                "Number": Number.S,
                "Person": Person["3"],
                "Tense": Tense.PRES,
                "Voice": Voice.ACTIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "am")
            self.assertEqual(analysis.inflections[0].affix, "at")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_quaero(self):
        result = self.par.parse("quaerebar")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "quaer")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.IND,
                "Number": Number.S,
                "Person": Person["1"],
                "Tense": Tense.IMPF,
                "Voice": Voice.PASSIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "quaer")
            self.assertEqual(analysis.inflections[0].affix, "ebar")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_tulisti(self):
        result = self.par.parse("tulisti")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "fer")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.IND,
                "Number": Number.S,
                "Person": Person["2"],
                "Tense": Tense.PERF,
                "Voice": Voice.ACTIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "tul")
            self.assertEqual(analysis.inflections[0].affix, "isti")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_amavisse(self):
        result = self.par.parse("amavisse")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "am")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.INF,
                "Number": Number.X,
                "Person": Person["0"],
                "Tense": Tense.PERF,
                "Voice": Voice.ACTIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "amav")
            self.assertEqual(analysis.inflections[0].affix, "isse")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_abiri(self):
        result = self.par.parse("abiri")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "abe")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.INF,
                "Number": Number.X,
                "Person": Person["0"],
                "Tense": Tense.PRES,
                "Voice": Voice.PASSIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "abi")
            self.assertEqual(analysis.inflections[0].affix, "ri")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_decet(self):
        result = self.par.parse("decet")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "dec")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.IND,
                "Number": Number.S,
                "Person": Person["3"],
                "Tense": Tense.PRES,
                "Voice": Voice.ACTIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "dec")
            self.assertEqual(analysis.inflections[0].affix, "et")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_alit(self):
        result = self.par.parse("alit")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "al")
            self.assertEqual(analysis.lexeme.wordType, WordType.V)

            self.assertEqual(len(analysis.inflections), 1)
            expected_features = {
                "Mood": Mood.IND,
                "Number": Number.S,
                "Person": Person["3"],
                "Tense": Tense.PRES,
                "Voice": Voice.ACTIVE,
            }
            self.assertEqual(analysis.inflections[0].stem, "al")
            self.assertEqual(analysis.inflections[0].affix, "it")
            self.assertEqual(analysis.inflections[0].wordType, WordType.V)
            self.assertEqual(analysis.inflections[0].features, expected_features)

    def test_venit(self):
        result = self.par.parse("venit")
        # response syntax and basics
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.wordType, WordType.V)
            if (
                analysis.lexeme.roots[0] == "vene"
            ):  # venere, venio = to be sold as a slave
                self.assertEqual(len(analysis.inflections), 1)
                expected_features = {
                    "Mood": Mood.IND,
                    "Number": Number.S,
                    "Person": Person["3"],
                    "Tense": Tense.PRES,
                    "Voice": Voice.ACTIVE,
                }
                self.assertEqual(analysis.inflections[0].stem, "veni")
                self.assertEqual(analysis.inflections[0].affix, "t")
                self.assertEqual(analysis.inflections[0].wordType, WordType.V)
                self.assertEqual(analysis.inflections[0].features, expected_features)
            elif analysis.lexeme.roots[0] == "veni":
                self.assertEqual(len(analysis.inflections), 2)
                for inflection in analysis.inflections:
                    self.assertEqual(analysis.inflections[0].stem, "ven")
                    self.assertEqual(analysis.inflections[0].affix, "it")
                    self.assertEqual(analysis.inflections[0].wordType, WordType.V)
                    self.assertTrue(inflection.has_feature(Mood.IND))
                    self.assertTrue(inflection.has_feature(Number.S))
                    self.assertTrue(inflection.has_feature(Person["3"]))
                    self.assertTrue(inflection.has_feature(Voice.ACTIVE))

                other_features = [x.features["Tense"] for x in analysis.inflections]
                self.assertTrue(Tense.PRES in other_features)
                self.assertTrue(Tense.PERF in other_features)
            else:
                self.fail("Invalid root")
