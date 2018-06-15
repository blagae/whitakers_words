"""
Parse.py (relating to Words's parse.adb)

Parse a word or list of input words and return word form and
definition

"""

__author__ = "Luke Hollis <luke@archimedes.digital>"
__license__ = "MIT License. See LICENSE."

import re
from copy import deepcopy
from open_words.constants import format_output
from open_words.exceptions import WordsException

try:
    from open_words.dict_id import WordsIds
    from open_words.dict_line import WordsDict
    from open_words.addons import LatinAddons
    from open_words.stem_list import Stems
    from open_words.uniques import Uniques
    from open_words.inflects import Inflects
except ImportError:
    from open_words.format_data import reimport_all_dicts
    reimport_all_dicts()
    from open_words.dict_id import WordsIds
    from open_words.dict_line import WordsDict
    from open_words.addons import LatinAddons
    from open_words.stem_list import Stems
    from open_words.uniques import Uniques
    from open_words.inflects import Inflects


class Parse:

    def __init__(self, **kwargs):
        """Provide a modular structure for loading the parser data"""
        self.wordlist = kwargs['wordlist'] if 'wordlist' in kwargs else WordsIds
        self.addons = kwargs['addons'] if 'addons' in kwargs else LatinAddons
        self.stems = kwargs['stems'] if 'stems' in kwargs else Stems
        self.uniques = kwargs['uniques'] if 'uniques' in kwargs else Uniques
        self.inflects = kwargs['inflects'] if 'inflects' in kwargs else Inflects
        self.wordkeys = kwargs['worddict'] if 'worddict' in kwargs else WordsDict

    def parse(self, word):
        """
        Parse an input string as a Latin word and look it up in the Words dictionary.

        Return dictionary and grammatical data formatted in a similar manner as original
        Words program.

        """
        if not word.isalpha():
            raise WordsException("Text to be parsed must be a single Latin word")

        out = []
        # Split enclitics
        options = self._split_enclitic(word)

        for option in options:
            # Check base word against list of uniques
            if option['base'] in self.uniques:
                for unique_form in self.uniques[option['base']]:
                    # TODO: stems shouldn't be empty
                    out.append({'w': unique_form, 'enclitic': option['encl'], 'stems': []})
            # Get regular words
            else:
                out.extend(self._find_forms(option))

        out = format_output(out)
        return {'word': word, 'defs': out}

    def _find_forms(self, option, reduced=False):
        infls = []
        out = []

        if option['base'] in self.wordkeys:
            ii = self.inflects["0"]['']
            infls.append(ii)

        # Check against inflection list
        max_inflect_length = min(7, len(option['base']))
        # range does not include the parameter number
        for length in reversed(range(1, max_inflect_length)):
            ending = option['base'][-length:]
            if ending in self.inflects[str(length)]:
                infl = self.inflects[str(length)][ending]

                infls.append(infl)

        # Run against stems
        stems = self._check_stems(option, infls)

        # Lookup dict info
        out.extend(self._lookup_stems(stems, not reduced))

        # If not already reduced, reduce the word and recurse
        if len(out) == 0 and not reduced:
            r_out = self._reduce(option)

            # If there's useful data after reducing, extend out w/data
            if r_out:
                out.extend(r_out)

        return out

    def _check_stems(self, option, infls):
        """
        For each inflection that was a match, remove the inflection from
        the end of the word string and then check the resulting stem
        against the list of stems loaded in __init__
        """
        match_stems = []

        # For each of the inflections that is a match, strip the inflection from the end of the word
        # and look up the stripped word (w) in the stems
        for infl_list in infls:
            if len(infl_list[0]['ending']):
                w = option['base'][:-len(infl_list[0]['ending'])]
            else:
                w = option['base']
            if w in self.stems:
                stem_list = self.stems[w]
                for stem in stem_list:
                    for infl in infl_list:
                        # If the inflection and stem identify as the same part of speech
                        if (
                                infl['pos'] == stem['pos']
                                or (
                                infl['pos'] == "VPAR"
                                and stem['pos'] == "V"
                        )
                        ):

                            # Ensure the inflections apply to the correct stem decl/conj/etc
                            if infl['n'][0] == stem['n'][0]:
                                is_in_match_stems = False

                                # If this stem is already in the match_stems list, add infl to that stem (if not already an infl in that stem list)
                                for i, mst in enumerate(match_stems):
                                    if stem == mst['st']:
                                        is_in_match_stems = True

                                        # So the matches a stem in the match_stems.  Is it unique to that stem's infls. If so, append it to that stem's infls.
                                        is_in_stem_infls = False
                                        for stem_infl in mst['infls']:
                                            if stem_infl['form'] == infl['form']:
                                                is_in_stem_infls = True
                                                # we found a match, stop looking
                                                break

                                        if not is_in_stem_infls:
                                            mst['infls'].append(infl)

                                if not is_in_match_stems:
                                    match_stems.append({'st': stem, 'infls': [infl], 'encl': option['encl']})

        return match_stems

    def _lookup_stems(self, match_stems, get_word_ends=True):
        """Find the word id mentioned in the stem in the dictionary"""
        out = []

        for stem in match_stems:
            try:
                word = self.wordlist[int(stem['st']['wid'])]
            except IndexError:
                continue
            if stem['st']['wid'] != word['id']:
                raise Exception("given key does not exist -- this exception should never occur")

            # If word already in out, add stem to word stems
            is_in_out = False
            for i, w in enumerate(out):
                if (
                        'id' in w['w'] and word['id'] == w['w']['id']
                        or
                        w['w']['orth'] == word['orth']
                ):

                    # It is in the out list already, flag and then check if the stem is already in the stems
                    is_in_out = True

                    # Ensure the stem is not already in the out word stems
                    is_in_out_word_stems = False
                    for st in out[i]['stems']:
                        if st == stem:
                            is_in_out_word_stems = True
                            # We have a match, break the loop
                            break

                    if not is_in_out_word_stems:
                        out[i]['stems'].append(stem)
                    # If we matched a word in the out, break the loop
                    break

            # If the word isn't in the out yet
            if not is_in_out:

                # Check the VPAR / V relationship
                if word['pos'] == "V":

                    # If the stem doesn't match the 4th principle part, it's not VPAR
                    if word['parts'].index(stem['st']['orth']) == 3:

                        # Remove "V" infls
                        stem = Parse.remove_extra_infls(stem, "V")

                    else:
                        # Remove "VPAR" infls
                        stem = Parse.remove_extra_infls(stem, "VPAR")

                # Lookup word ends
                # Need to Clone this object - otherwise self.wordlist is modified
                word_clone = deepcopy(word)
                if get_word_ends:
                    word_clone = self._get_word_endings(word_clone)

                # Finally, append new word to out
                out.append({'w': word_clone, 'enclitic': stem['encl'], 'stems': [stem]})

        return out

    def _split_enclitic(self, s):
        """Split enclitic ending from word"""
        out = [{'base': s, 'encl': ''}]

        # Test the different tackons / packons as specified in addons.py
        for e in self.addons['tackons']:
            if s.endswith(e['orth']):

                # Standardize data format
                e['form'] = e['orth']

                # Est exception
                if s != "est":
                    base = re.sub(e['orth'] + "$", "", s)
                    out.append({'base': base, 'encl': e, "stems": []})

        # which list do we get info from
        if s.startswith("qu"):
            lst = 'packons'
        else:
            lst = 'not_packons'

        for e in self.addons[lst]:
            if s.endswith(e['orth']):
                base = re.sub(e['orth'] + "$", "", s)
                # an enclitic without a base is not an enclitic
                if base:
                    out.append({'base': base, 'encl': e, "stems": []})
                    # avoid double entry for -cumque and -que
                    break

        return out

    def _get_word_endings(self, word):
        """
        Get the word endings for the stems in the Dictionary;
        eventually this should be phased out in favor of including the
        endings in the words in the dict_line dict
        """
        end_one = False
        end_two = False
        end_three = False
        end_four = False

        len_w_p = len(word['parts'])

        for key, infl_set in self.inflects.items():
            for ke, infl_list in self.inflects[key].items():
                for infl in infl_list:
                    # If the conjugation/declesion is a match AND the part of speech is a match (regularize V/VPAR)
                    if (
                            infl['n'] == word['n']
                            and (
                            infl['pos'] == word['pos']
                            or (
                                    infl['pos'] in ["V", "VPAR"]
                                    and word['pos'] in ["V", "VPAR"]
                            )
                    )
                    ):

                        # If the word is a verb, get the 4 principle parts
                        if word['pos'] in ["V", "VPAR"]:
                            # Pres act ind first singular
                            if len_w_p > 0 and not end_one and (len(word['parts'][0]) > 0 and word['parts'][0] != "-"):
                                if infl['form'] == "PRES  ACTIVE  IND  1 S":
                                    word['parts'][0] = word['parts'][0] + infl['ending']
                                    end_one = True

                            # Pres act inf
                            if len_w_p > 1 and not end_two and (len(word['parts'][1]) > 0 and word['parts'][1] != "-"):
                                if infl['form'] == "PRES  ACTIVE  INF  0 X":
                                    word['parts'][1] = word['parts'][1] + infl['ending']
                                    end_two = True

                            # Perf act ind first singular
                            if len_w_p > 2 and not end_three and (len(word['parts'][2]) > 0 and word['parts'][2] != "-"):
                                if infl['form'] == "PERF  ACTIVE  IND  1 S":
                                    word['parts'][2] = word['parts'][2] + infl['ending']
                                    end_three = True

                            # Perfect passive participle
                            if len_w_p > 3 and not end_four and (len(word['parts'][3]) > 0 and word['parts'][3] != "-"):
                                if infl['form'] == "NOM S M PRES PASSIVE PPL":
                                    word['parts'][3] = word['parts'][3] + infl['ending']
                                    end_four = True

                        # If the word is a noun or adjective, get the nominative and genetive singular forms
                        elif word['pos'] in ["N", "ADJ", "PRON"]:
                            # Nominative singular
                            if len_w_p > 0 and not end_one:
                                if infl['form'].startswith("NOM S") and (len(word['parts'][0]) > 0 and word['parts'][0] != "-"):
                                    word['parts'][0] = word['parts'][0] + infl['ending']
                                    end_one = True

                            # Genitive singular
                            if len_w_p > 1 and not end_two:
                                if infl['form'].startswith("GEN S") and (len(word['parts'][1]) > 0 and word['parts'][1] != "-"):
                                    word['parts'][1] = word['parts'][1] + infl['ending']
                                    end_two = True

        # Finish up a little bit of standardization for forms
        # For Verbs
        if word['pos'] in ["V", "VPAR"]:
            if len_w_p > 0 and not end_one:
                for inf in self.inflects:
                    if infl['form'] == "PRES  ACTIVE  IND  1 S" and infl['n'] == [0, 0] and (
                            len(word['parts'][0]) > 0 and word['parts'][0] != "-"):
                        word['parts'][0] = word['parts'][0] + infl['ending']
                        break

            if len_w_p > 1 and not end_two:
                for inf in self.inflects:
                    if infl['form'] == "PRES  ACTIVE  INF  0 X" and infl['n'] == [0, 0] and (
                            len(word['parts'][1]) > 0 and word['parts'][1] != "-"):
                        word['parts'][1] = word['parts'][1] + infl['ending']
                        break

            if len_w_p > 2 and not end_three:
                for inf in self.inflects:
                    if infl['form'] == "PERF  ACTIVE  IND  1 S" and infl['n'] == [0, 0] and (
                            len(word['parts'][2]) > 0 and word['parts'][2] != "-"):
                        word['parts'][2] = word['parts'][2] + infl['ending']
                        break

            if len_w_p > 3 and not end_four:
                for inf in self.inflects:
                    if infl['form'] == "NOM S M PERF PASSIVE PPL" and infl['n'] == [0, 0] and (
                            len(word['parts'][3]) > 0 and word['parts'][3] != "-"):
                        word['parts'][3] = word['parts'][3] + infl['ending']
                        break

        # Finish for nouns
        elif word['pos'] in ["N", "ADJ", "PRON"]:
            # Nominative singular
            if len_w_p > 0 and not end_one and infl['n'] == [0, 0] and (
                    len(word['parts'][0]) > 0 and word['parts'][0] != "-"):
                for inf in self.inflects:
                    if infl['form'].startswith("NOM S"):
                        word['parts'][0] = word['parts'][0] + infl['ending']
                        end_one = True

            # Genitive singular
            if len_w_p > 1 and not end_two and infl['n'] == [0, 0] and (
                    len(word['parts'][1]) > 0 and word['parts'][1] != "-"):
                for inf in self.inflects:
                    if infl['form'].startswith("GEN S"):
                        word['parts'][1] = word['parts'][1] + infl['ending']
                        end_two = True

        # If endings really don't exist, fall back to default
        if word['pos'] in ["V", "VPAR"]:
            if len_w_p > 0 and not end_one and (len(word['parts'][0]) > 0 and word['parts'][0] != "-"):
                word['parts'][0] = word['parts'][0] + "o"
            if len_w_p > 1 and not end_two and (len(word['parts'][1]) > 0 and word['parts'][1] != "-"):
                word['parts'][1] = word['parts'][1] + "?re"
            if len_w_p > 2 and not end_three and (len(word['parts'][2]) > 0 and word['parts'][2] != "-"):
                word['parts'][2] = word['parts'][2] + "i"
            if len_w_p > 3 and not end_four and (len(word['parts'][3]) > 0 and word['parts'][3] != "-"):
                word['parts'][3] = word['parts'][3] + "us"

        return word

    def _reduce(self, option):
        """Reduce the stem with suffixes and try again"""
        out = []
        found_new_match = False
        s = option['base']
        # For each inflection match, check prefixes and suffixes
        for prefix in self.addons['prefixes']:
            if s.startswith(prefix['orth']):
                s = re.sub("^" + prefix['orth'], "", s)
                out.append({'w': prefix, 'stems': [], 'addon': "prefix"})
                break
        for suffix in self.addons['suffixes']:
            if s.endswith(suffix['orth']):
                s = re.sub(suffix['orth'] + "$", "", s)
                out.append({'w': suffix, 'stems': [], 'addon': "suffix"})
                break

        # Find forms with the 'reduced' flag set to true
        option['base'] = s
        out = self._find_forms(option, True)

        # Has reducing input string given us useful data?
        # If not, return false
        for word in out:
            if len(word['stems']) > 0:
                found_new_match = True

        if out and not found_new_match:
            out = []

        return out

    @staticmethod
    def remove_extra_infls(stem, remove_type="VPAR"):
        """Remove Vs or VPARs from a list of inflections"""
        stem_infls_copy = stem['infls'][:]

        for infl in stem_infls_copy:
            if infl['pos'] == remove_type:
                stem['infls'].remove(infl)

        return stem
