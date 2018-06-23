from open_words.parse import Parser

import unittest


class MinimalTest(unittest.TestCase):
    @staticmethod
    def make_minimal_parse():
        return Parser(wordlist=[], addons=dict(), stems=[], uniques=[], inflects=dict(), wordkeys=dict())

    def test_empty(self):
        prs = MinimalTest.make_minimal_parse()
        result = prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_functional(self):
        prs = MinimalTest.make_minimal_parse()
        prs.wordkeys["word"] = {""}
        prs.inflects["0"] = {'': [{'ending': ''}]}
        result = prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_functional(self):
        prs = MinimalTest.make_minimal_parse()
        prs.wordkeys["word"] = {""}
        prs.inflects["0"] = {'': [{'ending': ''}]}
        result = prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)
