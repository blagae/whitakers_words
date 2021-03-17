from enum import Enum
from typing import Type
import inspect
import sys


def get_enum_or_dict(name: str) -> Type[Enum]:
    enum_class = [x[1] for x in names if x[0] == name]
    return enum_class[0]


def get_enum_value(object_name: str, value_name: str) -> Enum:
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
    X = "Unknown"


class Voice(Enum):
    ACTIVE = "Active"
    PASSIVE = "Passive"
    X = "Unknown"


class Mood(Enum):
    IND = "Indicative"
    SUB = "Subjunctive"
    IMP = "Imperative"
    INF = "Infinitive"
    X = "Unknown"


class Gender(Enum):
    M = "Masculine"
    F = "Feminine"
    N = "Neuter"
    C = "Common"
    X = "Unknown"


class Number(Enum):
    S = "Singular"
    P = "Plural"
    X = "Unknown"


class Case(Enum):
    NOM = "Nominative"
    VOC = "Vocative"
    GEN = "Genitive"
    DAT = "Dative"
    ACC = "Accusative"
    ABL = "Ablative"
    LOC = "Locative"
    X = "Unknown"


class Degree(Enum):
    POS = "Positive"
    COMP = "Comparative"
    SUPER = "Superlative"
    X = "Unknown"


# this has its problems, because we can't use Person.1, but we can use Person['1']
Person = Enum(value="Person", names=[('0', 0), ('1', 1), ('2', 2), ('3', 3)])


names = inspect.getmembers(sys.modules[__name__], inspect.isclass)
