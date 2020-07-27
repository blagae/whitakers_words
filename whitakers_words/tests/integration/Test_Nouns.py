from whitakers_words.parse import Parser

import unittest


class NounTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()

    def test_regionem(self):
        """
        expected = {'word': 'regionem',
                    'defs': [{'orth': ['regio', 'region'],
                              'senses': ['area, region', 'neighborhood', 'district, country', 'direction'],
                              'infls': [{'stem': 'region', 'ending': 'em', 'pos': 'noun',
                                         'form': {'case': 'accusative', 'number': 'singular', 'gender': 'feminine'}}]}]}
        """
        result = self.par.parse("regionem")

        # response syntax and basics
        self.assertEqual(len(result['defs']), 1)  # there is only one definition
        self.assertTrue(len(result['defs'][0]))  # defs does not contain an empty dictionary
        self.assertEqual(len(result['defs'][0]['infls']), 1)  # there is only one inflection

        # response splitting
        infl = result['defs'][0]['infls'][0]
        self.assertEqual(infl['stem'], 'region')
        self.assertEqual(infl['ending'], 'em')
        self.assertEqual(infl['pos'], 'noun')

        # response details
        form = infl['form']
        expected_form = {'case': 'accusative', 'number': 'singular', 'gender': 'feminine'}
        self.assertEqual(form, expected_form)
