from whitakers_words.parse import Parser

import unittest


class VerbTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_quaero(self):
        """
        expected = {'word': 'quaero',
                    'defs': [{'orth': ['quaero', 'quaerere', 'quaesivi', 'quaesitus'],
                              'senses': ['search for, seek, strive for', 'obtain', 'ask, inquire, demand'],
                              'infls': [{'stem': 'quaer', 'ending': 'o', 'pos': 'verb',
                                         'form': {'tense': 'present', 'voice': 'active', 'mood': 'indicative',
                                                  'person': 1, 'number': 'singular'}}]}]}
        """
        result = self.par.parse("quaero")
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
        expected_form = {'tense': 'present', 'voice': 'active', 'mood': 'indicative', 'person': 1, 'number': 'singular'}
        self.assertEqual(form, expected_form)
