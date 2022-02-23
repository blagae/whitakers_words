import unittest

from whitakers_words.enums import (
    Case,
    Gender,
    Mood,
    Number,
    Person,
    Tense,
    Voice,
    WordType,
)
from whitakers_words.parser import Parser


class VergiliusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_arma(self):
        result = self.par.parse("arma")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for analysis in result.forms[0].analyses.values():
            self.assertIn(analysis.lexeme.wordType, [WordType.N, WordType.V])
            self.assertEqual(analysis.lexeme.roots[0], "arm")

            if analysis.lexeme.wordType == WordType.N:
                self.assertEqual(len(analysis.inflections), 3)
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, "arm")
                    self.assertEqual(inflection.affix, "a")
                    self.assertEqual(inflection.wordType, WordType.N)
                    self.assertTrue(inflection.has_feature(Number.P))
                    # self.assertTrue(inflection.has_feature(Gender.M))
                other_features = [[x.features["Case"]] for x in analysis.inflections]
                self.assertTrue([Case.NOM] in other_features)
                self.assertTrue([Case.VOC] in other_features)
                self.assertTrue([Case.ACC] in other_features)
            else:
                self.assertEqual(len(analysis.inflections), 1)
                inflection = analysis.inflections[0]
                self.assertEqual(inflection.stem, "arm")
                self.assertEqual(inflection.affix, "a")
                self.assertEqual(inflection.wordType, WordType.V)
                self.assertTrue(inflection.has_feature(Mood.IMP))
                self.assertTrue(inflection.has_feature(Voice.ACTIVE))
                self.assertTrue(inflection.has_feature(Tense.PRES))
                self.assertTrue(inflection.has_feature(Person["2"]))
                self.assertTrue(inflection.has_feature(Number.S))

    def test_virumque(self):
        result = self.par.parse("virumque")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 3)
        self.assertEqual(result.forms[0].enclitic.text, "que")
        for analysis in result.forms[0].analyses.values():
            self.assertIn(analysis.lexeme.roots[0], ["vir", "vis"])
            if analysis.lexeme.roots[0] == "vir":
                if analysis.lexeme.category[1] == 3:
                    self.assertEqual(analysis.lexeme.wordType, WordType.N)

                    self.assertEqual(len(analysis.inflections), 1)
                    inflection = analysis.inflections[0]

                    self.assertEqual(inflection.stem, "vir")
                    self.assertEqual(inflection.affix, "um")
                    self.assertEqual(inflection.wordType, WordType.N)
                    self.assertTrue(inflection.has_feature(Case.ACC))
                    self.assertTrue(inflection.has_feature(Number.S))
                    self.assertTrue(inflection.has_feature(Gender.M))
                elif analysis.lexeme.category[1] == 2:
                    self.assertEqual(analysis.lexeme.wordType, WordType.N)

                    self.assertEqual(len(analysis.inflections), 3)

                    for inflection in analysis.inflections:
                        self.assertEqual(inflection.stem, "vir")
                        self.assertEqual(inflection.affix, "um")
                        self.assertEqual(inflection.wordType, WordType.N)
                        self.assertTrue(inflection.has_feature(Number.S))
                        self.assertTrue(inflection.has_feature(Gender.N))
                    other_features = [
                        [x.features["Case"]] for x in analysis.inflections
                    ]
                    self.assertTrue([Case.NOM] in other_features)
                    self.assertTrue([Case.ACC] in other_features)
                    self.assertTrue([Case.VOC] in other_features)
            elif analysis.lexeme.roots[0] == "vis":
                self.assertEqual(analysis.lexeme.wordType, WordType.N)

                self.assertEqual(len(analysis.inflections), 1)
                inflection = analysis.inflections[0]

                self.assertEqual(inflection.stem, "vir")
                self.assertEqual(inflection.affix, "um")
                self.assertEqual(inflection.wordType, WordType.N)
                self.assertTrue(inflection.has_feature(Case.GEN))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Gender.F))

    def test_cano(self):
        result = self.par.parse("cano")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 5)
        for analysis in result.forms[0].analyses.values():
            if analysis.lexeme.wordType == WordType.V:
                self.assertEqual(analysis.lexeme.roots[0], "can")
                self.assertEqual(len(analysis.inflections), 1)
                expected_features = {
                    "Mood": Mood.IND,
                    "Number": Number.S,
                    "Person": Person["1"],
                    "Tense": Tense.PRES,
                    "Voice": Voice.ACTIVE,
                }
                self.assertEqual(analysis.inflections[0].stem, "can")
                self.assertEqual(analysis.inflections[0].affix, "o")
                self.assertEqual(analysis.inflections[0].wordType, WordType.V)
                self.assertEqual(analysis.inflections[0].features, expected_features)
