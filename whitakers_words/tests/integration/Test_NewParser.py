from whitakers_words.new_parser import NewParser

import unittest


class NewParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.par = NewParser()

    def test_saevar(self):
        word = self.par.parse("amavit")
        self.assertTrue(word.text == "amavit")
