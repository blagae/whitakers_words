from open_words.parse import Parser

import unittest
import json


class VerbTest(unittest.TestCase):

    def __init__(self, meth):
        super().__init__(meth)
        self.par = Parser()

    def parse(self, word):
        return self.par.parse(word)

    def test_quaero(self):
        """
        expected = {'word': 'quaero',
                    'defs': [{'orth': ['quaero', 'quaerere', 'quaesivi', 'quaesitus'],
                              'senses': ['search for, seek, strive for', 'obtain', 'ask, inquire, demand'],
                              'infls': [{'stem': 'quaer', 'ending': 'o', 'pos': 'verb',
                                         'form': {'tense': 'present', 'voice': 'active', 'mood': 'indicative',
                                                  'person': 1, 'number': 'singular'}}]}]}
        """
        result = self.parse("quaero")
        # response syntax and basics
        self.assertEqual(len(result['defs']), 1)  # there is only one definition
        self.assertTrue(len(result['defs'][0]))  # defs does not contain an empty dictionary
        self.assertEqual(len(result['defs'][0]['infls']), 1)  # there is only one inflection

        # response splitting
        infl = result['defs'][0]['infls'][0]
        self.assertEqual(infl['stem'], 'quaer')
        self.assertEqual(infl['ending'], 'o')
        self.assertEqual(infl['pos'], 'verb')

        # response details
        form = infl['form']
        self.assertEqual(form['tense'], 'present')
        self.assertEqual(form['voice'], 'active')
        self.assertEqual(form['mood'], 'indicative')
        self.assertEqual(form['person'], 1)
        self.assertEqual(form['number'], 'singular')
