from open_words.parse import Parser

import unittest


class MinimalTest(unittest.TestCase):
    @staticmethod
    def make_minimal_parser():
        # make sure to create a new Parser for each test
        return Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=dict())

    def test_empty(self):
        prs = MinimalTest.make_minimal_parser()
        result = prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_functional(self):
        prs = MinimalTest.make_minimal_parser()
        prs.wordkeys["word"] = {""}
        prs.inflects["0"] = {'': [{'ending': ''}]}
        result = prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_with_result(self):
        prs = MinimalTest.make_minimal_parser()
        word = {'orth': 'word', 'pos': 'NUM', 'n': 'a', 'form': 'abc', 'wid': '0', 'parts': ['word'], 'senses': []}
        prs.wordkeys["word"] = word
        prs.inflects["0"] = {'': [{'ending': '', 'pos': 'NUM', 'n': 'a', 'form': ''}]}
        prs.stems["word"] = [word]
        prs.wordlist.append(word)
        result = prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'orth': ['word'], 'senses': [],
                              'infls': [{'stem': 'word', 'ending': '', 'pos': 'number', 'form': {'form': ['']}}]}]}
        self.assertEqual(result, expected)

    def test_minimal_empty_unique(self):
        prs = MinimalTest.make_minimal_parser()
        prs.uniques['word'] = []
        result = prs.parse("word")
        expected = {'word': 'word',
                    'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_unique_with_result(self):
        prs = MinimalTest.make_minimal_parser()
        word = {'orth': 'word', 'pos': 'NUM', 'form': 'abc', 'senses': []}
        prs.uniques['word'] = [word]
        result = prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'orth': ['word'], 'senses': [],
                              'infls': [{'form': {'form': ['abc']}, 'ending': '', 'pos': 'number'}]}]}
        self.assertEqual(result, expected)

    def test_minimal_unique_with_addon(self):
        prs = MinimalTest.make_minimal_parser()
        word = {'orth': 'wor', 'pos': 'NUM', 'form': 'abc', 'senses': []}
        prs.uniques['wor'] = [word]
        prs.addons['tackons'] = [{'orth': 'd'}]
        result = prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'enclitic': {'form': 'd', 'orth': 'd'},
                              'infls': [{'ending': '',
                                         'form': {'form': ['abc']},
                                         'pos': 'number'}],
                              'orth': ['wor'],
                              'senses': []}]}
        self.assertEqual(result, expected)
