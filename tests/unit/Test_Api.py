import unittest

from whitakers_words.datatypes import DictEntry, Unique
from whitakers_words.enums import WordType
from whitakers_words.parser import Form, Parser, Word


class MinimalDictionaryParseTest(unittest.TestCase):

    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=set())

    def test_empty(self):
        result = self.prs.parse("word")
        self.assertEqual(result.forms, [])

    def test_minimal_functional(self):
        self.prs.data.wordkeys.add("")
        self.prs.data.inflects["0"] = {'': [{'ending': ''}]}
        result = self.prs.parse("word")
        self.assertEqual(result.forms, [])

    def test_minimal_with_result(self):
        word: DictEntry = {'orth': 'word', 'pos': 'NUM', 'n': ['a'], 'form': 'abc',
                           'wid': 0, 'parts': ['word'], 'senses': []}
        self.prs.data.wordkeys.add("word")
        self.prs.data.empty = {'NUM': [{'ending': '', 'pos': 'NUM', 'n': ['a'], 'form': '', 'iid': 0, 'stem': 0}]}
        self.prs.data.stems["word"] = [word]
        self.prs.data.wordlist.append(word)
        result = self.prs.parse("word")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        self.assertEqual(result.forms[0].analyses[0].lexeme.category, ['a'])
        self.assertEqual(result.forms[0].analyses[0].lexeme.wordType, WordType.NUM)
        self.assertEqual(len(result.forms[0].analyses[0].inflections), 1)
        self.assertEqual(result.forms[0].analyses[0].inflections[0].category, ['a'])
        self.assertEqual(result.forms[0].analyses[0].inflections[0].wordType, WordType.NUM)

    def test_minimal_empty_unique(self):
        self.prs.data.uniques['word'] = []
        result = self.prs.parse("word")
        self.assertEqual(result.forms, [])

    def test_minimal_unique_with_result(self):
        word: Unique = {'orth': 'word', 'pos': 'PREP', 'n': [], 'form': 'a cdef', 'senses': []}
        self.prs.data.uniques['word'] = [word]
        result = self.prs.parse("word")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(len(result.forms[0].analyses), 1)
        self.assertEqual(result.forms[0].analyses[0].lexeme.category, [])
        self.assertEqual(result.forms[0].analyses[0].lexeme.wordType, WordType.PREP)

    def test_minimal_unique_with_addon(self):
        word = {'orth': 'wor', 'pos': 'PREP', 'form': 'abc', 'senses': []}
        self.prs.data.uniques['wor'] = [word]
        self.prs.data.addons['tackons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        result = self.prs.parse("word")
        self.assertEqual(len(result.forms), 1)
        self.assertEqual(result.forms[0].enclitic.text, 'd')
        self.assertEqual(result.forms[0].text, 'wor')
        self.assertEqual(len(result.forms[0].analyses), 1)
        self.assertEqual(result.forms[0].analyses[0].lexeme.category, [])
        self.assertEqual(result.forms[0].analyses[0].lexeme.wordType, WordType.PREP)


class MinimalDictionaryAnalyzeFormsTest(unittest.TestCase):
    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=set())

    def test_empty(self):
        form = Form("word")
        form.analyse(self.prs.data)
        self.assertEqual(form.analyses, {})


class MinimalDictionarySplitFormEnclitic(unittest.TestCase):
    def setUp(self):
        # make sure to create a new Parser for each test
        self.prs = Parser(wordlist=[], addons=dict(), stems=dict(), uniques=dict(), inflects=dict(), wordkeys=set())

    def test_empty(self):
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0].text, "word")

    def test_tackon(self):
        self.prs.data.addons['tackons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0].text, "word")
        self.assertEqual(forms[1].text, "wor")
        self.assertEqual(forms[1].enclitic.text, "d")

    def test_packon(self):
        self.prs.data.addons['packons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        forms = Word("quword").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0].text, "quword")
        self.assertEqual(forms[1].text, "quwor")
        self.assertEqual(forms[1].enclitic.text, "d")

    def test_not_packon(self):
        self.prs.data.addons['not_packons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 2)
        self.assertEqual(forms[0].text, "word")
        self.assertEqual(forms[1].text, "wor")
        self.assertEqual(forms[1].enclitic.text, "d")

    def test_nonexisting_not_packon(self):
        self.prs.data.addons['packons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0].text, "word")

    def test_nonexisting_packon(self):
        self.prs.data.addons['not_packons'] = [{'orth': 'd', 'pos': '', 'senses': []}]
        forms = Word("quword").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0].text, "quword")

    def test_double_tackon(self):
        self.prs.data.addons['tackons'] = [{'orth': 'd', 'pos': '', 'senses': []},
                                           {'orth': 'rd', 'pos': '', 'senses': []}]
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 3)
        self.assertEqual(forms[0].text, "word")
        self.assertEqual(forms[1].text, "wor")
        self.assertEqual(forms[1].enclitic.text, "d")
        self.assertEqual(forms[2].text, "wo")
        self.assertEqual(forms[2].enclitic.text, "rd")

    def test_double_packon(self):
        self.prs.data.addons['packons'] = [{'orth': 'd', 'pos': '', 'senses': []},
                                           {'orth': 'rd', 'pos': '', 'senses': []}]
        forms = Word("quword").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 3)
        self.assertEqual(forms[0].text, "quword")
        self.assertEqual(forms[1].text, "quwor")
        self.assertEqual(forms[1].enclitic.text, "d")
        self.assertEqual(forms[2].text, "quwo")
        self.assertEqual(forms[2].enclitic.text, "rd")

    def test_double_not_packon(self):
        self.prs.data.addons['not_packons'] = [{'orth': 'd', 'pos': '', 'senses': []},
                                               {'orth': 'rd', 'pos': '', 'senses': []}]
        forms = Word("word").split_form_enclitic(self.prs.data)
        self.assertEqual(len(forms), 3)
        self.assertEqual(forms[0].text, "word")
        self.assertEqual(forms[1].text, "wor")
        self.assertEqual(forms[1].enclitic.text, "d")
        self.assertEqual(forms[2].text, "wo")
        self.assertEqual(forms[2].enclitic.text, "rd")
