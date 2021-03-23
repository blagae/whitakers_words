import unittest

from whitakers_words.enums import WordType
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

    def test_esse(self):
        result = self.par.parse("sum")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        analysis = result.forms[0].analyses[0]
        self.assertEqual(len(analysis.inflections), 1)
        self.assertIsInstance(analysis.inflections[0], UniqueInflection)
        self.assertIsInstance(analysis.lexeme, UniqueLexeme)
        self.assertEqual(analysis.lexeme.wordType, WordType.V)
