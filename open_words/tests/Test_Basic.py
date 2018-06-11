from open_words.parse import Parse

import unittest
import json


class CrashTest(unittest.TestCase):

    def __init__(self, meth):
        super().__init__(meth)
        self.par = Parse()

    def parse(self, word):
        print(json.dumps(self.par.parse(word), indent=2))

    def test_unique(self):
        self.parse("quodcumque")

    def test_esse(self):
        self.parse("sum")

    def test_regular(self):
        self.parse("cecidit")

    def test_immutable(self):
        self.parse("et")

    def test_vol(self):
        self.parse("vult")

    def test_optional_enclitic(self):
        self.parse("pollice")

    def test_pronoun(self):
        self.parse("se")

    def test_preposition(self):
        self.parse("super")

    def test_personal_pronoun(self):
        self.parse("tu")

    def test_aen(self):
        words = dict()
        filename = "aeneis.txt"
        with open(filename, encoding="ISO-8859-1") as f:
            for line in f:
                for word in line.split():
                    try:
                        # don't print
                        self.par.parse(word)
                    except:
                        if word in words:
                            words[word] += 1
                        else:
                            words[word] = 1
        print(len(words))
        total = 0
        for k, v in words.items():
            print(k)
            total += v
        print(total)
