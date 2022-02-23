import unittest

from whitakers_words.enums import Case, Gender, Number, WordType
from whitakers_words.parser import Parser


class PronounTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_pronoun(self):
        result = self.par.parse("se")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "-")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 2)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "s")
                self.assertEqual(inflection.affix, "e")
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.C))
                self.assertTrue(inflection.has_feature(Number.X))

            other_features = [[x.features["Case"]] for x in analysis.inflections]
            self.assertTrue([Case.ACC] in other_features)
            self.assertTrue([Case.ABL] in other_features)

    def test_personal_pronoun(self):
        result = self.par.parse("tu")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "tu")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 2)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "tu")
                self.assertEqual(inflection.affix, "")
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.C))
                self.assertTrue(inflection.has_feature(Number.S))

            other_features = [[x.features["Case"]] for x in analysis.inflections]
            self.assertTrue([Case.NOM] in other_features)
            self.assertTrue([Case.VOC] in other_features)

    def test_quos(self):
        result = self.par.parse("quos")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 31)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "qu")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "qu")
                self.assertEqual(inflection.affix, "os")
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Gender.M))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Case.ACC))

    def test_tuas(self):
        result = self.par.parse("tuas")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "tu")
            # adjectival pronoun
            self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "tu")
                self.assertEqual(inflection.affix, "as")
                self.assertEqual(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Gender.F))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Case.ACC))

    def test_ea(self):
        result = self.par.parse("ea")
        self.assertEqual(len(result.forms), 1)
        # TODO fix medieval hit for 'eare', and -dem
        self.assertEqual(len(result.forms[0].analyses), 3)
        for analysis in result.forms[0].analyses.values():
            if analysis.lexeme.wordType == WordType.V or len(analysis.inflections) > 4:
                continue
            self.assertEqual(analysis.lexeme.roots[0], "i")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 4)
            # common properties
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "e")
                self.assertEqual(inflection.affix, "a")
                self.assertEqual(inflection.wordType, WordType.PRON)

            features = [
                [x.features["Case"], x.features["Number"], x.features["Gender"]]
                for x in analysis.inflections
            ]
            self.assertTrue([Case.NOM, Number.P, Gender.N] in features)
            self.assertTrue([Case.ACC, Number.P, Gender.N] in features)
            self.assertTrue([Case.NOM, Number.S, Gender.F] in features)
            self.assertTrue([Case.ABL, Number.S, Gender.F] in features)

    def test_ipsum(self):
        result = self.par.parse("ipsum")
        self.assertEqual(len(result.forms), 1)
        # TODO fix medieval hit for 'eare', and -dem
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "ips")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 3)
            # common properties
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "ips")
                self.assertEqual(inflection.affix, "um")
                self.assertEqual(inflection.wordType, WordType.PRON)
                self.assertTrue(inflection.has_feature(Number.S))

            other_features = [
                [x.features["Case"], x.features["Gender"]] for x in analysis.inflections
            ]
            self.assertTrue([Case.NOM, Gender.N] in other_features)
            self.assertTrue([Case.ACC, Gender.N] in other_features)
            self.assertTrue([Case.ACC, Gender.M] in other_features)

    def test_ipsa(self):
        result = self.par.parse("ipsa")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "ips")
            self.assertEqual(analysis.lexeme.wordType, WordType.PRON)

            self.assertEqual(len(analysis.inflections), 4)
            # common properties
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "ips")
                self.assertEqual(inflection.affix, "a")
                self.assertEqual(inflection.wordType, WordType.PRON)

            features = [
                [x.features["Case"], x.features["Number"], x.features["Gender"]]
                for x in analysis.inflections
            ]
            self.assertTrue([Case.NOM, Number.S, Gender.F] in features)
            self.assertTrue([Case.NOM, Number.P, Gender.N] in features)
            self.assertTrue([Case.ACC, Number.P, Gender.N] in features)
            self.assertTrue([Case.ABL, Number.S, Gender.F] in features)
