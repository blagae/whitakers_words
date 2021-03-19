import re
from enum import Enum
from typing import Any, Sequence

from whitakers_words.data.addons import addons
from whitakers_words.datatypes import Addon, DictEntry, Inflect, Stem, Unique
from whitakers_words.enums import WordType, get_enum_value
from whitakers_words.generated.dict_ids import dict_ids as wordlist
from whitakers_words.generated.dict_keys import dict_keys as wordkeys
from whitakers_words.generated.inflects import inflects
from whitakers_words.generated.stems import stems
from whitakers_words.generated.uniques import uniques


class DataLayer:
    def __init__(self, **kwargs: Any):
        self.wordlist = kwargs['wordlist'] if 'wordlist' in kwargs else wordlist
        self.wordkeys = kwargs['wordkeys'] if 'wordkeys' in kwargs else wordkeys
        self.stems = kwargs['stems'] if 'stems' in kwargs else stems
        self.uniques = kwargs['uniques'] if 'uniques' in kwargs else uniques
        self.inflects = kwargs['inflects'] if 'inflects' in kwargs else inflects
        self.addons = kwargs['addons'] if 'addons' in kwargs else addons


class Inflection:
    def __init__(self, infl: Inflect, stem_lemma: str):
        self.wordType = get_enum_value("WordType", infl["pos"])
        self.category = infl['n']
        self.stem = stem_lemma
        self.affix = infl["ending"]
        self.features: dict[str, Enum] = {}
        self.analyse_features(infl["form"])

    def analyse_features(self, features: Sequence[str]) -> None:
        if self.wordType in [WordType.N, WordType.PRON, WordType.NUM]:
            lst = ["Case", "Number", "Gender"]
        elif self.wordType == WordType.ADJ:
            lst = ["Case", "Number", "Gender", "Degree"]
        elif self.wordType == WordType.V:
            lst = ["Tense", "Voice", "Mood", "Person", "Number"]
        elif self.wordType == WordType.VPAR:
            lst = ["Case", "Number", "Gender", "Tense", "Voice"]
        elif self.wordType == WordType.ADV:
            lst = ["Degree"]
        else:
            return
        for idx, feature in enumerate(features):  # TODO will break horribly
            self.features[lst[idx]] = get_enum_value(lst[idx], feature)

    def has_feature(self, feature: Enum) -> bool:
        return (type(feature).__name__ in self.features and
                self.features[type(feature).__name__] == feature)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inflection):
            return NotImplemented
        return (self.affix == other.affix and
                self.wordType == other.wordType and
                self.category == other.category and
                self.features == other.features)


class Lexeme:
    def __init__(self, stem: Stem):
        self.id = stem['wid']
        self.category = stem['n']
        self.roots: Sequence[str] = []
        self.senses: Sequence[str] = []
        self.wordType = get_enum_value("WordType", stem["pos"])


class Enclitic:
    def __init__(self, enclitic: Addon):
        self.text = enclitic['orth']
        self.position = enclitic['pos']
        self.meaning = enclitic['senses']


class Analysis:
    def __init__(self, lexeme: Lexeme, inflections: list[Inflection] = [], enclitic: Enclitic = None):
        self.lexeme = lexeme
        self.root = ""
        self.inflections = inflections
        self.enclitic = enclitic

    def lookup_stem(self, wordlist: Sequence[DictEntry]) -> None:
        dict_word = wordlist[self.lexeme.id]
        if dict_word:  # guard for empty entries
            self.lexeme.roots = dict_word["parts"]
            self.lexeme.senses = dict_word["senses"]


class Form:
    def __init__(self, text: str, enclitic: Enclitic = None):
        self.text = text
        self.analyses: dict[int, Analysis] = {}
        self.enclitic = enclitic

    def analyse_unique(self, unique_form: Unique) -> None:
        pass  # TODO

    def analyse(self, data: DataLayer) -> None:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        viable_inflections: list[Inflect] = []

        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        if self.text in data.wordkeys:
            viable_inflections.extend(data.inflects["0"][''])

        # Check against inflection list
        for inflect_length in range(1, min(8, len(self.text))):
            end_of_word = self.text[-inflect_length:]
            if str(inflect_length) in data.inflects and end_of_word in data.inflects[str(inflect_length)]:
                infl = data.inflects[str(inflect_length)][end_of_word]
                viable_inflections.extend(infl)

        # Get viable combinations of stem + endings (+ enclitics)
        analyses = self.match_stems_inflections(viable_inflections, data)

        for analysis in analyses.values():
            analysis.enclitic = self.enclitic
            analysis.lookup_stem(data.wordlist)
        # only use analyses where the lexeme was found
        self.analyses = dict(filter(lambda x: x[1].lexeme.roots, analyses.items()))

        # TODO reimplement reduce

    def match_stems_inflections(self, viable_inflections: Sequence[Inflect], data: DataLayer) -> dict[int, Analysis]:
        """
        For each inflection that was a theoretical match, remove the inflection from the end of the word string
        and then check the resulting stem against the list of stems loaded in __init__
        """
        matched_stems: dict[int, Analysis] = {}
        # For each of the inflections that is a match, strip the inflection from the end of the word
        # and look up the stripped word (w) in the stems
        for infl_cand in viable_inflections:
            ending_length = len(infl_cand['ending'])
            if ending_length:
                stem_lemma = self.text[:-ending_length]
            else:
                stem_lemma = self.text
            if stem_lemma in data.stems:
                stem_list = data.stems[stem_lemma]
                for stem_cand in stem_list:
                    wrd = data.wordlist[stem_cand['wid']]
                    if wrd and self.check_match(stem_cand, infl_cand, wrd):
                        word_id = stem_cand['wid']
                        inflection = Inflection(infl_cand, stem_lemma)
                        # If there's already a matched stem with that orthography
                        if word_id in matched_stems:
                            if inflection not in matched_stems[word_id].inflections:
                                matched_stems[word_id].inflections.append(inflection)
                        else:
                            matched_stems[word_id] = Analysis(Lexeme(stem_cand), [inflection])
        return matched_stems

    def check_match(self, stem: Stem, infl: Inflect, wrd: DictEntry) -> bool:  # TODO rewrite to be readable
        """ Do custom checking mechanisms to see if the inflection and stem identify as the same part of speech """
        if infl['pos'] != stem['pos']:
            if infl['pos'] == "VPAR" and stem['pos'] == "V":
                if infl['form'][0] == "PERF":
                    return stem['orth'] == wrd['parts'][-1]
                else:
                    return stem['orth'] == wrd['parts'][0]
            return False
        basic_match = len(stem['n']) > 0 and (infl['n'][0] == stem['n'][0] or infl['n'][0] == 0)
        if stem['pos'] == 'N':
            if infl['n'] == stem['n'] or (infl['n'][0] == stem['n'][0] and infl['n'][-1] == 0):
                return infl['form'][-1] == stem['form'][0] or infl['form'][-1] == 'C'
            return False
        elif stem['pos'] == 'ADV':
            if stem['form'] == ['X']:
                if stem['orth'] in wrd['parts']:
                    return get_degree(wrd['parts'], stem['orth']) == infl['form']
            return stem['form'] == infl['form']
        elif stem['pos'] == 'ADJ':
            if not basic_match:
                return False
            if stem['form'][-1] == 'X':
                if stem['orth'] in wrd['parts']:
                    return get_degree(wrd['parts'][1:], stem['orth'])[0] == infl['form'][-1]
            return stem['form'] == infl['form']  # TODO we're now only checking pos/comp/super
        return basic_match


degrees = {
    "POS": {"id": 0, "name": "positive"},
    "COMP": {"id": 1, "name": "comparative"},
    "SUPER": {"id": 2, "name": "superlative"}
}


def get_degree(parts: Sequence[str], stem: str) -> list[str]:  # TODO replace
    val = [key for (key, value) in degrees.items() if value['id'] == parts.index(stem)]
    return val


class Word:
    def __init__(self, text: str):
        self.text = text
        self.forms: Sequence[Form] = []

    def analyse(self, data: DataLayer) -> 'Word':
        form_candidates = self.split_form_enclitic()
        for form in form_candidates:
            if form.text in data.uniques:
                for unique_form in data.uniques[form.text]:
                    form.analyse_unique(unique_form)
            # Get regular words
            else:
                form.analyse(data)
        # only use forms that get at least one valid analysis
        self.forms = list(filter(lambda form: form.analyses, form_candidates))
        return self

    def split_form_enclitic(self) -> Sequence[Form]:
        """Split enclitic ending from word"""
        result = [Form(self.text)]  # TODO form with enclitic will fail to be parsed

        # Test the different tackons / packons as specified in addons.py
        result.extend(self.find_enclitic('tackons'))

        # which list do we get info from
        if self.text.startswith("qu"):
            result.extend(self.find_enclitic('packons'))
        else:
            result.extend(self.find_enclitic('not_packons'))
        return result

    def find_enclitic(self, list_name: str) -> Sequence[Form]:
        if list_name in addons:
            for affix in addons[list_name]:
                affix_text = affix['orth']
                if self.text.endswith(affix_text):
                    base = re.sub(affix_text + "$", "", self.text)
                    # an enclitic without a base is not an enclitic
                    if base:
                        return [Form(base, Enclitic(affix))]
        return []

    def get_analyses(self) -> Sequence[Analysis]:
        return [item for form in self.forms for item in form.analyses.values()]


class Parser:
    def __init__(self, **kwargs: Any):
        self.data = DataLayer(**kwargs)

    def parse(self, text: str) -> Word:
        return Word(text).analyse(self.data)
