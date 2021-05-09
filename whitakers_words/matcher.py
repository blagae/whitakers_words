from typing import Callable

from .datatypes import Inflect, Stem
from .enums import Degree, NumeralType


class Matcher:
    def __init__(self, stem: Stem, infl: Inflect):
        self.stem = stem
        self.infl = infl
        self.function: Callable[[Stem, Inflect], bool]
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
        elif stem["pos"] == "PRON":
            self.function = _pronoun_checker
        else:
            self.function = _basic_matcher

    def check(self) -> bool:
        return self.function(self.stem, self.infl)


def _check_right_stem(stem: Stem, infl: Inflect) -> bool:
    return stem["stem_number"] == infl["stem"]


def _dummy_false(stem: Stem, infl: Inflect) -> bool:
    return False


def _vpar_checker(stem: Stem, infl: Inflect) -> bool:
    return _check_right_stem(stem, infl)


def _noun_checker(stem: Stem, infl: Inflect) -> bool:
    if _check_right_stem(stem, infl):
        if infl["n"] == stem["n"] or (infl["n"][0] == stem["n"][0] and infl["n"][-1] == 0):
            return (infl["form"][-1] in ("X", stem["form"][0]) or
                    (infl["form"][-1] == "C" and stem["form"][0] in ("F", "M")))
    return False


def _adj_checker(stem: Stem, infl: Inflect) -> bool:
    if not _basic_matcher(stem, infl) or not _check_right_stem(stem, infl):
        return False
    if stem["form"][-1] == "X":
        return Degree.get_degree_list()[max(0, stem["stem_number"]-1)] == infl["form"][-1]
    return stem["form"][-1] == infl["form"][-1]


def _adv_checker(stem: Stem, infl: Inflect) -> bool:
    if stem["form"] == ["X"]:
        return Degree.get_degree_list()[stem["stem_number"]] == infl["form"][-1]
    return stem["form"] == infl["form"]


def _verb_checker(stem: Stem, infl: Inflect) -> bool:
    if stem["form"][0] in ("IMPERS", "DEP", "SEMIDEP", "PERFDEF"):
        if not _special_verb_checker(stem, infl):
            return False
    return _basic_matcher(stem, infl) and _check_right_stem(stem, infl)


def _special_verb_checker(stem: Stem, infl: Inflect) -> bool:
    if stem["form"][0] == "IMPERS":  # e.g. decet
        return infl["form"][-2] == "3"
    if stem["form"][0] == "DEP":  # e.g. tueri
        return infl["form"][1] == "PASSIVE"
    if stem["form"][0] == "SEMIDEP":  # e.g. audeo, ausus sum
        if infl["form"][1] == "PASSIVE":
            return infl["form"][0] in ("PERF", "FUTP", "PLUP")  # TODO will this ever hit ?
        return infl["form"][0] in ("PRES", "IMP", "FUT")
    if stem["form"][0] == "PERFDEF":  # e.g. coepisse
        return infl["form"][0] in ("PERF", "FUTP", "PLUP")
    return True


def _numeral_checker(stem: Stem, infl: Inflect) -> bool:
    return (_basic_matcher(stem, infl) and
            (stem["form"][0] == infl["form"][-1] or
             (stem["form"][0] == 'X' and NumeralType.get_type_list()[stem["stem_number"]] == infl["form"][-1])))


def _pronoun_checker(stem: Stem, infl: Inflect) -> bool:
    return _check_right_stem(stem, infl) and infl["n"] == stem["n"]


def _basic_matcher(stem: Stem, infl: Inflect) -> bool:
    if stem["n"]:
        return (infl["n"] == stem["n"] or infl["n"][0] == 0 or
                (infl["n"][0] == stem["n"][0] and infl["n"][1] == 0))
    return True
