import inspect
import sys
from enum import Enum
from typing import Type


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

    @classmethod
    def get_degree_list(cls) -> list[str]:
        return [x.name for x in Degree]


# this has its problems, because we can't use Person.1, but we can use Person["1"]
Person = Enum(value="Person", names=[("0", 0), ("1", 1), ("2", 2), ("3", 3)])


class PronounType(Enum):
    REFLEX = "Reflexive"
    DEMONS = "Demonstrative"
    INDEF = "Indefinite"
    PERS = "Personal"
    INTERR = "Interrogative"
    REL = "Relative"
    ADJECT = "Adjectival"
    X = "Unknown"


class FilterCriteria(Enum):
    AGE = 0
    AREA = 1
    GEO = 2
    FREQ = 3
    SOURCE = 4


# https://mk270.github.io/whitakers-words/dictionary.html
class Age(Enum):
    X = "DEFAULT"     # In use throughout the ages/unknown # the default
    A = "Archaic"     # Very early forms, obsolete by classical times
    B = "Early"       # Early Latin, pre-classical, used for effect/poetry
    C = "Classical"   # Limited to classical (~150 BC - 200 AD)
    D = "Late"        # Late, post-classical (3rd-5th centuries)
    E = "Later"       # Latin not in use in Classical times (6-10) Christian
    F = "Medieval"    # Medieval (11th-15th centuries)
    G = "Scholar"     # Latin post 15th - Scholarly/Scientific   (16-18)
    H = "Modern"      # Coined recently, words for new things (19-20)


class Area(Enum):
    X = "Default"
    A = "Agriculture"   # Flora, Fauna, Land, Equipment, Rural
    B = "Biological"    # Medical, Body Parts
    D = "Drama"         # Music, Theater, Art, Painting, Sculpture
    E = "Ecclesiastic"  # Biblical, Religious
    G = "Grammar"       # Rhetoric, Logic, Literature, Schools
    L = "Legal"         # Government, Tax, Financial, Political, Titles
    P = "Poetic"
    S = "Science"       # Philosophy, Mathematics, Units/Measures
    T = "Technical"     # Architecture, Topography, Surveying
    W = "War"           # Military, Naval, Ships, Armor
    Y = "Mythology"


class Geography(Enum):
    X = "Default"
    A = "Africa"
    B = "Britain"
    C = "China"
    D = "Scandinavia"
    E = "Egypt"
    F = "France, Gaul"
    G = "Germany"
    H = "Greece"
    I = "Italy, Rome"  # noqa: E741
    J = "India"
    K = "Balkans"
    N = "Netherlands"
    P = "Persia"
    Q = "Near East"
    R = "Russia"
    S = "Spain, Iberia"
    U = "Eastern Europe"


class Frequency(Enum):
    A = "Very Frequent"  # full column or more, more than 50 citations - very frequent
    B = "Frequent"       # half column, more than 20 citations - frequent
    C = "Common"         # more then 5 citations - common
    D = "Uncommon"       # 4-5 citations - lesser
    E = "Rare"           # 2-3 citations - uncommon
    F = "Very Rare"      # only 1 citation - very rare
    I = "Inscription"    # Only citation is inscription  # noqa: E741
    M = "Graffiti"       # Presently not much used
    N = "Plinius"        # Things that appear only in Plinius Natural History


class Source(Enum):
    X = "General or unknown or too common to say"
    A = "Unused 1"
    B = "C.H.Beeson, A Primer of Medieval Latin, 1925 (Bee)"
    C = "Charles Beard, Cassell's Latin Dictionary 1892 (CAS)"
    D = "J.N.Adams, Latin Sexual Vocabulary, 1982 (Sex)"
    E = "L.F.Stelten, Dictionary of Eccles. Latin, 1995 (Ecc)"
    F = "Roy J. Deferrari, Dictionary of St. Thomas Aquinas, 1960 (DeF)"
    G = "Gildersleeve + Lodge, Latin Grammar 1895 (G+L)"
    H = "Collatinus Dictionary by Yves Ouvrard"
    I = "Leverett, F.P., Lexicon of the Latin Language, Boston 1845"  # noqa: E741
    J = "Unused 2"
    K = "Calepinus Novus, modern Latin, by Guy Licoppe (Cal)"
    L = "Lewis, C.S., Elementary Latin Dictionary 1891"
    M = "Latham, Revised Medieval Word List, 1980"
    N = "Lynn Nelson, Wordlist"
    O = "Oxford Latin Dictionary, 1982 (OLD)"  # noqa: E741
    P = "Souter, A Glossary of Later Latin to 600 A.D., Oxford 1949"
    Q = "Other, cited or unspecified dictionaries"
    R = "Plater & White, A Grammar of the Vulgate, Oxford 1926"
    S = "Lewis and Short, A Latin Dictionary, 1879 (L+S)"
    T = "Found in a translation  --  no dictionary reference"
    U = "Du Cange"
    V = "Vademecum in opus Saxonis - Franz Blatt (Saxo)"
    W = "My personal guess"
    Y = "Temp special code"
    Z = "Sent by user"  # no dictionary reference


# TODO other types
"""
subtypes = {
    "N": ["M", "N", "T", "P", "F", "W", "C", "A", "L", "G", "X"],
    "PREP": ["ABL", "ACC", "GEN"], "ADJ": ["POS", "X", "SUPER", "COMP"],
    "V": ["INTRANS", "TRANS", "X", "SEMIDEP", "DEP", "TO_BEING", "IMPERS", "DAT", "ABL", "PERFDEF"],
    "ADV": ["POS", "X", "SUPER", "COMP"],
    "PRON": ["INDEF", "ADJECT", "PERS", "DEMONS", "X", "REL", "INTERR", "REFLEX"],
    "NUM": ["CARD", "X", "DIST", "ORD", "ADVERB"],
    "PACK": ["REL", "INTERR", "INDEF", "ADJECT"]
}
"""


names = inspect.getmembers(sys.modules[__name__], inspect.isclass)
