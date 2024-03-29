import unittest

from whitakers_words.enums import Case, Degree, Gender, Number, WordType
from whitakers_words.parser import Parser


class AdjectiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_saevissimae(self):
        result = self.par.parse("saevissimae")

        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "saev")
            self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEqual(len(analysis.inflections), 4)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "saevissi")
                self.assertEqual(inflection.affix, "mae")
                self.assertEqual(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Degree.SUPER))
                self.assertTrue(inflection.has_feature(Gender.F))

            other_features = [
                [x.features["Case"], x.features["Number"]] for x in analysis.inflections
            ]
            self.assertTrue([Case.GEN, Number.S] in other_features)
            self.assertTrue([Case.DAT, Number.S] in other_features)
            self.assertTrue([Case.VOC, Number.P] in other_features)
            self.assertTrue([Case.NOM, Number.P] in other_features)

    def test_bonorum(self):
        result = self.par.parse("bonorum")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 3)
        for analysis in result.forms[0].analyses.values():
            if analysis.lexeme.wordType == WordType.ADJ:
                self.assertEqual(analysis.lexeme.roots[0], "bon")
                self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

                self.assertEqual(len(analysis.inflections), 2)
                # common properties and features
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, "bon")
                    self.assertEqual(inflection.affix, "orum")
                    self.assertEqual(inflection.wordType, WordType.ADJ)
                    self.assertTrue(inflection.has_feature(Degree.POS))
                    self.assertTrue(inflection.has_feature(Case.GEN))
                    self.assertTrue(inflection.has_feature(Number.P))

                other_features = [x.features["Gender"] for x in analysis.inflections]
                self.assertTrue(Gender.M in other_features)
                self.assertTrue(Gender.N in other_features)

    def test_felicium(self):
        result = self.par.parse("felicium")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "felix")
            self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "felic")
                self.assertEqual(inflection.affix, "ium")
                self.assertEqual(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Degree.POS))
                self.assertTrue(inflection.has_feature(Case.GEN))
                self.assertTrue(inflection.has_feature(Number.P))
                self.assertTrue(inflection.has_feature(Gender.X))

    def test_melius(self):
        result = self.par.parse("melius")

        self.assertEqual(len(result.forms), 1)
        # see Test_Adverbs.test_melius
        self.assertEqual(len(result.forms[0].analyses), 2)
        analysis = result.forms[0].analyses[6825]
        self.assertEqual(analysis.lexeme.roots[0], "bon")
        self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

        self.assertEqual(len(analysis.inflections), 3)
        # common properties and features
        for inflection in analysis.inflections:
            self.assertEqual(inflection.stem, "meli")
            self.assertEqual(inflection.affix, "us")
            self.assertEqual(inflection.wordType, WordType.ADJ)
            self.assertTrue(inflection.has_feature(Degree.COMP))
            self.assertTrue(inflection.has_feature(Gender.N))
            self.assertTrue(inflection.has_feature(Number.S))

        other_features = [x.features["Case"] for x in analysis.inflections]
        self.assertTrue(Case.VOC in other_features)
        self.assertTrue(Case.ACC in other_features)
        self.assertTrue(Case.NOM in other_features)

    def test_anceps(self):
        result = self.par.parse("anceps")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        for analysis in result.forms[0].analyses.values():
            self.assertEqual(analysis.lexeme.roots[0], "anceps")
            self.assertEqual(analysis.lexeme.wordType, WordType.ADJ)

            self.assertEqual(len(analysis.inflections), 3)
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, "anceps")
                self.assertEqual(inflection.affix, "")
                self.assertEqual(inflection.wordType, WordType.ADJ)
                self.assertTrue(inflection.has_feature(Degree.POS))
                self.assertTrue(inflection.has_feature(Number.S))

            other_features = [x.features["Case"] for x in analysis.inflections]
            self.assertTrue(Case.VOC in other_features)
            self.assertTrue(Case.NOM in other_features)

    def test_acer(self):
        result = self.par.parse("acer")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 2)
        for analysis in result.forms[0].analyses.values():
            if analysis.lexeme.wordType == WordType.ADJ:
                self.assertEqual(analysis.lexeme.roots[0], "acer")

                self.assertEqual(len(analysis.inflections), 2)
                for inflection in analysis.inflections:
                    self.assertEqual(inflection.stem, "acer")
                    self.assertEqual(inflection.affix, "")
                    self.assertEqual(inflection.wordType, WordType.ADJ)
                    self.assertTrue(inflection.has_feature(Degree.POS))
                    self.assertTrue(inflection.has_feature(Number.S))
                    self.assertTrue(inflection.has_feature(Gender.M))

                other_features = [x.features["Case"] for x in analysis.inflections]
                self.assertTrue(Case.VOC in other_features)
                self.assertTrue(Case.NOM in other_features)
