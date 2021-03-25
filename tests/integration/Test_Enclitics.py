import unittest

from whitakers_words.enums import WordType
from whitakers_words.parser import Parser


class EncliticTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_unique(self):
        result = self.par.parse("quodcumque")
        self.assertEqual(len(result.forms), 1)  # also pollice
        self.assertEqual(result.forms[0].enclitic.text, 'cumque')
        self.assertEqual(len(result.forms[0].analyses), 6)
        for key, analysis in result.forms[0].analyses.items():
            self.assertTrue(analysis.lexeme.roots[0] in ['qu', 'quod'])  # wid == 6360

            # common properties and features
            for inflection in analysis.inflections:
                self.assertTrue(inflection.stem in ['qu', 'quod'])
                self.assertTrue(inflection.affix in ['', 'od'])

    def test_optional_enclitic(self):
        result = self.par.parse("pollice")
        self.assertEqual(len(result.forms), 2)  # also pollice
        self.assertEqual(result.forms[1].enclitic.text, 'ce')
        self.assertEqual(len(result.forms[1].analyses), 3)
        for key, analysis in result.forms[1].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'poll')  # wid == 6360

            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'poll')
                self.assertEqual(inflection.affix, 'i')


    def test_be_ne(self):
        result = self.par.parse("bene")
        self.assertEqual(len(result.forms), 2)  # also bene
        self.assertEqual(result.forms[1].enclitic.text, 'ne')
        self.assertEqual(len(result.forms[1].analyses), 1)
        for key, analysis in result.forms[1].analyses.items():
            self.assertEqual(analysis.lexeme.roots[0], 'be')  # wid == 6360
            self.assertEqual(analysis.lexeme.wordType, WordType.INTERJ)

            self.assertEqual(len(analysis.inflections), 1)
            # common properties and features
            for inflection in analysis.inflections:
                self.assertEqual(inflection.stem, 'be')
                self.assertEqual(inflection.affix, '')
                self.assertEqual(inflection.wordType, WordType.INTERJ)
                self.assertFalse(inflection.features)
