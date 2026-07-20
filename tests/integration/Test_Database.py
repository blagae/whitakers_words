import concurrent.futures
import os
import unittest

from whitakers_words.datalayer import (FileBasedDataLayer, MySqlDataLayer,
                                       SqliteDataLayer)
from whitakers_words.formatter import JsonFormatter
from whitakers_words.parser import Parser

mysql_url = os.environ.get("WW_MYSQL_URL")

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


@unittest.skipUnless(mysql_url, "WW_MYSQL_URL not set")
class MySqlLayerTest(unittest.TestCase):
    """
    Verify that the MySQL database layer gives the exact same results as the
    dictionary-based layer (see BUILDING/README for generating the ww_* tables)
    """

    @classmethod
    def setUpClass(cls):
        cls.dict_parser = Parser()
        cls.db_parser = Parser(database=mysql_url)
        cls.formatter = JsonFormatter()

    def test_layer_type(self):
        self.assertIsInstance(self.db_parser.data, MySqlDataLayer)

    def test_identical_results(self):
        for word in words:
            with self.subTest(word=word):
                expected = self.formatter.format_result(self.dict_parser.parse(word))
                actual = self.formatter.format_result(self.db_parser.parse(word))
                self.assertEqual(expected, actual)

    def test_identical_results_full_frequency(self):
        dict_parser = Parser(frequency="X")
        db_parser = Parser(frequency="X", database=mysql_url)
        for word in words:
            with self.subTest(word=word):
                expected = self.formatter.format_result(dict_parser.parse(word))
                actual = self.formatter.format_result(db_parser.parse(word))
                self.assertEqual(expected, actual)

    def test_concurrent_use_from_multiple_threads(self):
        """ one MySqlDataLayer instance is shared across requests by callers
        that cache a default parser (elisio.word._get_default_parser), which
        a threaded ASGI server then calls from a different worker thread per
        request; a single shared pymysql connection corrupts under that
        (regression: versescanner's review UI 500ing on the second/third
        verse loaded in a row) """
        layer = self.db_parser.data
        self.assertIsInstance(layer, MySqlDataLayer)
        repeated = words * 5
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
            futures = [pool.submit(layer.get_uniques, word) for word in repeated]
            errors = [future.exception() for future in futures if future.exception()]
        self.assertEqual(errors, [])
