from whitakers_words.parse import Parser

import unittest


class MinimalDictionaryParseTest(unittest.TestCase):

    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=dict())

    def test_empty(self):
        result = self.prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_functional(self):
        self.prs.wordkeys["word"] = {""}
        self.prs.inflects["0"] = {'': [{'ending': ''}]}
        result = self.prs.parse("word")
        expected = {'word': 'word', 'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_with_result(self):
        word = {'orth': 'word', 'pos': 'NUM', 'n': 'a', 'form': 'abc', 'wid': '0', 'parts': ['word'], 'senses': []}
        self.prs.wordkeys["word"] = word
        self.prs.inflects["0"] = {'': [{'ending': '', 'pos': 'NUM', 'n': 'a', 'form': ''}]}
        self.prs.stems["word"] = [word]
        self.prs.wordlist.append(word)
        result = self.prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'orth': ['word'], 'senses': [],
                              'infls': [{'stem': 'word', 'ending': '', 'pos': 'number', 'form': {'form': ['']}}]}]}
        self.assertEqual(result, expected)

    def test_minimal_empty_unique(self):
        self.prs.uniques['word'] = []
        result = self.prs.parse("word")
        expected = {'word': 'word',
                    'defs': []}
        self.assertEqual(result, expected)

    def test_minimal_unique_with_result(self):
        word = {'orth': 'word', 'pos': 'NUM', 'form': ['abc'], 'senses': []}
        self.prs.uniques['word'] = [word]
        result = self.prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'orth': ['word'], 'senses': [],
                              'infls': [{'form': {'form': ['abc']}, 'ending': '', 'pos': 'number'}]}]}
        self.assertEqual(result, expected)

    def test_minimal_unique_with_addon(self):
        word = {'orth': 'wor', 'pos': 'NUM', 'form': ['abc'], 'senses': []}
        self.prs.uniques['wor'] = [word]
        self.prs.addons['tackons'] = [{'orth': 'd'}]
        result = self.prs.parse("word")
        expected = {'word': 'word',
                    'defs': [{'enclitic': {'orth': 'd'},
                              'infls': [{'ending': '',
                                         'form': {'form': ['abc']},
                                         'pos': 'number'}],
                              'orth': ['wor'],
                              'senses': []}]}
        self.assertEqual(result, expected)


class MinimalDictionaryAnalyzeFormsTest(unittest.TestCase):
    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=dict())

    def test_empty(self):
        result = self.prs.analyze_forms({"base": "word"})
        expected = []
        self.assertEqual(result, expected)


class MinimalDictionarySplitFromEnclitic(unittest.TestCase):
    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=dict())

    def test_empty(self):
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""}]
        self.assertEqual(result, expected)

    def test_tackon(self):
        self.prs.addons['tackons'] = [{'orth': 'd'}]
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""}, {"base": "wor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)

    def test_packon(self):
        self.prs.addons['packons'] = [{'orth': 'd'}]
        result = self.prs.split_form_enclitic("quword")
        expected = [{"base": "quword", "encl": ""}, {"base": "quwor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)

    def test_not_packon(self):
        self.prs.addons['not_packons'] = [{'orth': 'd'}]
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""}, {"base": "wor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)

    def test_nonexisting_not_packon(self):
        self.prs.addons['packons'] = [{'orth': 'd'}]
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""}]
        self.assertEqual(result, expected)

    def test_nonexisting_packon(self):
        self.prs.addons['not_packons'] = [{'orth': 'd'}]
        result = self.prs.split_form_enclitic("quword")
        expected = [{"base": "quword", "encl": ""}]
        self.assertEqual(result, expected)

    def test_double_tackon(self):
        self.prs.addons['tackons'] = [{'orth': 'd'}, {'orth': 'd'}]
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""},
                    {"base": "wor", "encl": {'orth': 'd'}},
                    {"base": "wor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)

    def test_double_packon(self):
        self.prs.addons['packons'] = [{'orth': 'd'}, {'orth': 'd'}]
        result = self.prs.split_form_enclitic("quword")
        expected = [{"base": "quword", "encl": ""}, {"base": "quwor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)

    def test_double_not_packon(self):
        self.prs.addons['not_packons'] = [{'orth': 'd'}, {'orth': 'd'}]
        result = self.prs.split_form_enclitic("word")
        expected = [{"base": "word", "encl": ""}, {"base": "wor", "encl": {'orth': 'd'}}]
        self.assertEqual(result, expected)
