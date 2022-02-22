import unittest

from whitakers_words.formatter import JsonFormatter, WordsFormatter, YamlFormatter
from whitakers_words.parser import Parser


class FormatterTest(unittest.TestCase):
    """For now, just make sure that there's no weird exceptions in these formatters"""

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_jsonformat(self):
        word = self.par.parse("reginaque")
        result = JsonFormatter().format_result(word)
        print(result)

    def test_wordformat(self):
        word = self.par.parse("reginaque")
        result = WordsFormatter().format_result(word)
        print(result)

    def test_yamlformat(self):
        word = self.par.parse("reginaque")
        result = YamlFormatter().format_result(word)
        print(result)
