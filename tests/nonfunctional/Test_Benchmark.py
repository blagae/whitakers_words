import unittest
from datetime import timedelta
from timeit import default_timer as timer

from whitakers_words.parser import Parser


class PerformanceTest(unittest.TestCase):
    """
    A test class that makes sure that the parser is not mutated
    """

    @classmethod
    def setUpClass(cls):
        cls.par = Parser()
        cls.full_par = Parser(frequency="X")

    def test_meaningless_benchmark(self):
        start1 = timer()
        self.full_par.parse("amabat")
        end1 = timer()
        wat1 = timedelta(seconds=end1 - start1)
        start2 = timer()
        self.par.parse("amabat")
        end2 = timer()
        wat2 = timedelta(seconds=end2 - start2)
        self.assertTrue(
            abs((wat2 - wat1) / wat2) < 5
        )  # TODO super-flaky & doesn't mean anything
