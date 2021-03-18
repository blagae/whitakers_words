from whitakers_words.parser import Parser
from whitakers_words.enums import Case, Gender, Number, WordType

import unittest


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
