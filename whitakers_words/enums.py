from enum import Enum
import inspect
import sys

def get_enum_or_dict(name):
    enum_class = [x[1] for x in names if x[0] == name]
    return enum_class[0]


def get_enum_value(object_name, value_name):
    return get_enum_or_dict(object_name)[value_name]


class WordType(Enum):
    ADJ = "Adjective"
    ADV = "Adverb"
    CONJ = "Conjunction"
    INTERJ = "Interjection"
    N = "Noun"
    NUM = "Numeral"
    PREP = "Preposition"
    PRON = "Pronoun"
    V = "Verb"
    VPAR = "Verbal Participle"


class Tense(Enum):
    PRES = "Praesens"
    IMPF = "Imperfectum"
    PERF = "Perfectum"
    FUT = "Futurum Simplex"
    FUTP = "Futurum Exactum"
    PLUP = "Plusquamperfectum"


class Voice(Enum):
    ACTIVE = "Active"
    PASSIVE = "Passive"


class Mood(Enum):
    IND = "Indicative"
    SUB = "Subjunctive"
    IMP = "Imperative"
    INF = "Infinitive"


class Gender(Enum):
    M = "Masculine"
    F = "Feminine"
    N = "Neuter"
    C = "Common"


class Number(Enum):
    S = "Singular"
    P = "Plural"


class Case(Enum):
    NOM = "Nominative"
    VOC = "Vocative"
    GEN = "Genitive"
    DAT = "Dative"
    ACC = "Accusative"
    ABL = "Ablative"
    LOC = "Locative"

class Degree(Enum):
    POS = "Positive"
    COMP = "Comparative"
    SUPER = "Superlative"

Person = {"1": 1, "2": 2, "3": 3}


names = inspect.getmembers(sys.modules[__name__])
