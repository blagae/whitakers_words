
tenses = {
    'PRES': "present",
    'IMPF': "imperfect",
    'PERF': "perfect",
    'FUT': "future",
    'FUTP': "future perfect",
    'PLUP': "pluperfect",
    'INF': "infinitive",
    'X': ""
}
voices = {
    'ACTIVE': "active",
    'PASSIVE': "passive",
    'X': ""
}

moods = {
    'IND': "indicative",
    'SUB': "subjunctive",
    'IMP': "imperative",
    'INF': "infinitive",
    'X': ""
}

genders = {
    'M': "masculine",
    'F': "feminine",
    'N': "neuter",
    'C': "C",
    'X': ""
}

numbers = {
    'S': "singular",
    'P': "plural",
    'X': ""
}

declensions = {
    'NOM': "nominative",
    'VOC': "vocative",
    'GEN': "genitive",
    'DAT': "dative",
    'ACC': "accusative",
    'LOC': "locative",
    'ABL': "ablative",
    'X': ""
}


parts_of_speech = {
    "N": "noun",
    "V": "verb",
    "VPAR": "participle",
    "ADJ": "adjective",
    "ADV": "adverb",
    "PRON": "pronoun",
    "INTERJ": "interjection",
    "NUM": "number",
    "CONJ": "conjunction",
    "PREP": "preposition"
}


def format_form(form, pos):
    """
    Format form data to be more useful and relevant

    Nouns, Verbs, Adjectives, Participles(, Adverbs, Conjunctions, Prepositions)

    Nouns, Adjectives
     - declension: nominative, vocative, genitive, accusative, dative, ablative, locative
     - gender: male, female, neuter
     - number: singular, plural

    Verbs
     - person: 1, 2, 3
     - number: singular, plural
     - mood: indicative, subjunctive
     - voice: active, passive
     - tense: present, imperfect, perfect, future, future perfect, pluperfect, infinitive, imperative

    Participles
     - declension: nominative, vocative, genitive, accusative, dative, ablative, locative
     - gender: male, female, neuter
     - number: singular, plural
     - tense: present, perfect, future
     - voice: active, passive

    """
    if pos in ["N", "PRON", "ADJ", "NUM"]:
        # Ex. "ACC S C"
        form = form.split(" ")
        if len(form) == 3:
            formatted = {
                'declension': trans_declension(form[0]),
                'number': trans_number(form[1]),
                'gender': trans_gender(form[2])
            }
        else:
            formatted = {
                'form': form
            }

    elif pos == "V":
        # Ex: "FUT   ACTIVE  IND  3 S"
        if len(form) == 22:
            formatted = {
                'tense': trans_tense(form[0:6].strip()),
                'voice': trans_voice(form[6:14].strip()),
                'mood': trans_mood(form[14:19].strip()),
                'person': int(form[19:21].strip()),
                'number': trans_number(form[21:].strip())
            }
        else:
            formatted = {
                'form': form
            }

    elif pos == "VPAR":
        # Ex: "VOC P N PRES ACTIVE  PPL"
        if len(form) == 24:
            formatted = {
                'declension': trans_declension(form[0:4].strip()),
                'number': trans_number(form[4:6].strip()),
                'gender': trans_gender(form[6:8].strip()),
                'tense': trans_tense(form[8:13].strip()),
                'voice': trans_voice(form[13:21].strip())
            }
        else:
            formatted = {
                'form': form
            }

    elif pos in ["ADV", "INTERJ", "CONJ", "PREP", "X", "P"]:
        formatted = {
            'form': form
        }

    else:
        formatted = {
            'form': form
        }

    return formatted


def trans_declension(abb):
    return declensions[abb]


def trans_number(abb):
    return numbers[abb]


def trans_gender(abb):
    return genders[abb]


def trans_mood(abb):
    return moods[abb]


def trans_voice(abb):
    return voices[abb]


def trans_tense(abb):
    return tenses[abb]


def trans_pos(abb):
    return parts_of_speech[abb]


def format_morph(word):
    """
    Format the morphological data of the word forms into a more semantically useful model
    """

    for infl in word['infls']:
        # Translate form
        infl['form'] = format_form(infl['form'], infl['pos'])

        # Set part of speech
        infl['pos'] = trans_pos(infl['pos'])

    return word


def format_output(out):
    """Format the output in the designated type"""
    new_out = []

    for word in out:
        obj = {
            'orth': [],
            'senses': word['w']['senses'],
            'infls': []
        }
        if word['enclitic']:
            obj['enclitic'] = word['enclitic']
        # Format the orth of the new object
        if 'parts' in word['w']:
            obj['orth'] = word['w']['parts']
        else:
            obj['orth'] = [word['w']['orth']]

        # Format the stems / inflections of the new object
        if 'stems' in word:
            for stem in word['stems']:
                to_add_infls = []
                for infl in stem['infls']:

                    # Ensure the infl isn't already in the infls
                    is_in_formatted_infls = False
                    for formatted_infl in to_add_infls:
                        if infl['form'] == formatted_infl['form']:
                            is_in_formatted_infls = True

                    if not is_in_formatted_infls:
                        to_add_infls.append({
                            'stem': stem['st']['orth'],
                            'ending': infl['ending'],
                            'pos': infl['pos'],
                            'form': infl['form']
                        })

                for formatted_infl in to_add_infls:
                    if formatted_infl not in obj['infls']:
                        obj['infls'].append(formatted_infl)

        else:
            word['w']['form'] = word['w']['pos']

        # If we still don't have any inflections associated with the object
        if len(obj['infls']) == 0:
            obj['infls'] = [{
                'form': word['w']['form'],
                'ending': '',
                'pos': word['w']['pos']
            }]

        # Format the morphological data for the word forms into a more useful output
        obj = format_morph(obj)

        new_out.append(obj)

    return new_out

