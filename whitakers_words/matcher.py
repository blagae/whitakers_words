from typing import Callable, Sequence

from .datatypes import DictEntry, Inflect, Stem
from .enums import Degree, NumeralType


class Matcher:
    def __init__(self, stem: Stem, infl: Inflect):
        self.stem = stem
        self.infl = infl
        self.function: Callable[[Stem, Inflect, DictEntry], bool]
        if infl["pos"] != stem["pos"]:
            if infl["pos"] == "VPAR" and stem["pos"] == "V":
                self.function = _vpar_checker
            else:
                self.function = _dummy_false
        elif stem["pos"] == "N":
            self.function = _noun_checker
        elif stem["pos"] == "ADV":
            self.function = _adv_checker
        elif stem["pos"] == "ADJ":
            self.function = _adj_checker
        elif stem["pos"] == "V":
            self.function = _verb_checker
        elif stem["pos"] == "NUM":
            self.function = _numeral_checker
        else:
            self.function = _basic_matcher

    def check(self, word: DictEntry) -> bool:
        return self.function(self.stem, self.infl, word)


def _check_right_stem(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    return len(word["parts"]) > infl["stem"] and stem["orth"] == word["parts"][infl["stem"]]


def _dummy_false(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    return False


def _vpar_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    return _check_right_stem(stem, infl, word)


def _noun_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    if _check_right_stem(stem, infl, word):
        if infl["n"] == stem["n"] or (infl["n"][0] == stem["n"][0] and infl["n"][-1] == 0):
            return (infl["form"][-1] in ("X", stem["form"][0]) or
                    (infl["form"][-1] == "C" and stem["form"][0] in ("F", "M")))
    return False


# TODO clear up situation with "ADJ X" vs "ADJ POS"
def _adj_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    if not _basic_matcher(stem, infl, word):
        return False
    if stem["form"][-1] == "X":
        if stem["orth"] in word["parts"]:
            return get_degree(word["parts"][1:], stem["orth"]) == infl["form"][-1]
    return stem["form"][-1] == infl["form"][-1]


def _adv_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    if stem["form"] == ["X"]:
        if stem["orth"] in word["parts"]:
            return get_degree(word["parts"], stem["orth"]) == infl["form"][-1]
    return stem["form"] == infl["form"]


def _verb_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    return _basic_matcher(stem, infl, word) and _check_right_stem(stem, infl, word)


def _numeral_checker(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    return (_basic_matcher(stem, infl, word) and
            (stem["form"][0] == infl["form"][-1] or
             (stem["form"][0] == 'X' and get_numeral_type(word["parts"], stem["orth"]) == infl["form"][-1])))


def _basic_matcher(stem: Stem, infl: Inflect, word: DictEntry) -> bool:
    if stem["n"]:
        return (infl["n"] == stem["n"] or infl["n"][0] == 0 or
                (infl["n"][0] == stem["n"][0] and infl["n"][1] == 0))
    return True


def get_degree(parts: Sequence[str], stem: str) -> str:
    try:
        return Degree.get_degree_list()[parts.index(stem)]
    except ValueError:
        return Degree.POS.name


def get_numeral_type(parts: Sequence[str], stem: str):
    try:
        return NumeralType.get_type_list()[parts.index(stem)]
    except ValueError:
        return NumeralType.CARD.name
