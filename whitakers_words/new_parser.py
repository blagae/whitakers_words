import re
from typing import Any

from whitakers_words.generated.dict_ids import dict_ids as wordlist
from whitakers_words.generated.dict_keys import dict_keys as wordkeys
from whitakers_words.generated.stems import stems
from whitakers_words.generated.uniques import uniques
from whitakers_words.generated.inflects import inflects
from whitakers_words.data.addons import addons
from whitakers_words.enums import get_enum_value, WordType


class Inflection(object):
    def __init__(self, infl_dict: dict[str, str]):
        self.wordType = get_enum_value("WordType", infl_dict["pos"])
        self.category = infl_dict['n']
        self.affix = infl_dict["ending"]
        self.features: dict[str, Any] = {}
        self.analyse_features(infl_dict["form"])

    def analyse_features(self, features: str) -> None:
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
            lst = []
        for idx, feature in enumerate(features): # TODO will break horribly
            self.features[lst[idx]] = get_enum_value(lst[idx], feature)

class Lexeme(object):
    def __init__(self, stem: dict[str, str]):
        self.id = stem['wid']
        self.category = stem['n']
        self.roots: list[str] = []
        self.senses: list[str] = []
        self.wordType = get_enum_value("WordType", stem["pos"])

    def lookup_stem(self):
        """Find the word id mentioned in the stem in the dictionary"""
        dict_word = wordlist[self.id]
        self.roots = dict_word["parts"]
        self.senses = dict_word["senses"]


class Enclitic(object):
    def __init__(self, enclitic: dict[str, str]):
        self.text = enclitic['orth']
        self.position = enclitic['pos']
        self.meaning = enclitic['senses']


class Analysis(object):
    def __init__(self, lexeme: Lexeme, inflections: list[Inflection] = [], enclitic: Enclitic = None):
        self.lexeme = lexeme
        self.root = ""
        self.inflections = inflections
        self.enclitic = enclitic

    def lookup_stem(self) -> None:
        self.lexeme.lookup_stem()


class Form(object):
    def __init__(self, text: str, enclitic: Enclitic = None):
        self.text = text
        self.analyses: list[Analysis] = []
        self.enclitic = enclitic

    def analyse_unique(self, unique_form) -> None:
        pass  # TODO

    def analyse(self) -> None:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        viable_inflections: list[dict[str, Any]] = []

        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        if self.text in wordkeys:
            viable_inflections.append(inflects["0"][''])

        # Check against inflection list
        for inflect_length in range(1, min(8, len(self.text))):
            end_of_word = self.text[-inflect_length:]
            if str(inflect_length) in inflects and end_of_word in inflects[str(inflect_length)]:
                infl = inflects[str(inflect_length)][end_of_word]
                viable_inflections.append(infl)

        # Get viable combinations of stem + endings (+ enclitics)
        self.analyses = self.match_stems_inflections(viable_inflections)

        for analysis in self.analyses.values():
            analysis.enclitic = self.enclitic
            analysis.lookup_stem()

        # TODO reimplement reduce


    def match_stems_inflections(self, viable_inflections: list[dict[str, Any]]) -> dict[int, Analysis]:
        """
        For each inflection that was a theoretical match, remove the inflection from the end of the word string
        and then check the resulting stem against the list of stems loaded in __init__
        """
        matched_stems: dict[int, Analysis] = {}
        # For each of the inflections that is a match, strip the inflection from the end of the word
        # and look up the stripped word (w) in the stems
        for infl_lemma in viable_inflections:
            ending_length = len(infl_lemma[0]['ending'])
            if ending_length:
                stem_lemma = self.text[:-ending_length]
            else:
                stem_lemma = self.text
            if stem_lemma in stems:
                stem_list = stems[stem_lemma]
                for stem_cand in stem_list:
                    for infl_cand in infl_lemma:
                        if self.check_match(stem_cand, infl_cand):
                            word_id = stem_cand['wid']
                            inflection = Inflection(infl_cand)
                            # If there's already a matched stem with that orthography
                            if word_id in matched_stems:
                                matched_stems[word_id].inflections.append(inflection)
                            else:
                                matched_stems[word_id] = Analysis(Lexeme(stem_cand), [inflection])
        return matched_stems

    def check_match(self, a, b) -> bool:
        return True  # TODO fix this elegantly

class Word(object):
    def __init__(self, text: str):
        self.text = text
        self.forms = self.split_form_enclitic()

    def analyse(self) -> 'Word':
        for form in self.forms:
            if form.text in uniques:
                for unique_form in uniques[form.text]:
                    form.analyse_unique(unique_form)
            # Get regular words
            else:
                form.analyse()
        return self

    def split_form_enclitic(self) -> list[Form]:
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

    def find_enclitic(self, list_name: str) -> list[Form]:
        if list_name in addons:
            for suffix in addons[list_name]:
                if self.text.endswith(suffix['orth']):
                    base = re.sub(suffix['orth'] + "$", "", self.text)
                    # an enclitic without a base is not an enclitic
                    if base:
                        return [Form(base, Enclitic(suffix))]
        return []

    def analyses(self) -> list[Analysis]:
        return [item for form in self.forms for item in form.analyses]


class NewParser(object):
    def parse(self, text) -> Word:
        return Word(text).analyse()
