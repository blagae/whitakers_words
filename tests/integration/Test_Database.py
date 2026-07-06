import unittest

from whitakers_words.datalayer import FileBasedDataLayer, SqliteDataLayer
from whitakers_words.formatter import JsonFormatter
from whitakers_words.parser import Parser

words = [
    "amabat",
    "habes",
    "regis",
    "cornu",
    "didone",
    "vobiscum",
    "non",
    "que",
    "quibuscum",
    "cuius",
    "canentis",
    "amantissimi",
    "prompsi",
    "ait",
    "fortior",
]


class DatabaseLayerTest(unittest.TestCase):
    """
    Verify that the sqlite database layer gives the exact same results as the
    dictionary-based layer
    """

    @classmethod
    def setUpClass(cls):
        cls.dict_parser = Parser()
        cls.db_parser = Parser(database=True)
        cls.formatter = JsonFormatter()

    def test_layer_types(self):
        self.assertIsInstance(self.dict_parser.data, FileBasedDataLayer)
        self.assertIsInstance(self.db_parser.data, SqliteDataLayer)

    def test_identical_results(self):
        for word in words:
            with self.subTest(word=word):
                expected = self.formatter.format_result(self.dict_parser.parse(word))
                actual = self.formatter.format_result(self.db_parser.parse(word))
                self.assertEqual(expected, actual)

    def test_identical_results_full_frequency(self):
        dict_parser = Parser(frequency="X")
        db_parser = Parser(frequency="X", database=True)
        for word in words:
            with self.subTest(word=word):
                expected = self.formatter.format_result(dict_parser.parse(word))
                actual = self.formatter.format_result(db_parser.parse(word))
                self.assertEqual(expected, actual)
