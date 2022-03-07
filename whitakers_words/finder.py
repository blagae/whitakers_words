from enum import Enum
from typing import Sequence, Union
from whitakers_words.enums import WordType
from whitakers_words.generated.paradigms import paradigms


# TODO heavy refactoring
def find_inflection(wordType: Enum, n: Sequence[Union[str, int]], form: Sequence[Union[str, int]]) -> str:
    spec_cat = str(10 * int(n[0]) + int(n[1]))
    gen_cat = str(10 * int(n[0]))
    form_str = " ".join([str(x) for x in form]).upper()
    typ = wordType.name
    inflects = []
    if wordType == WordType.N:
        if spec_cat in paradigms[typ]:
            if form_str in paradigms[typ][spec_cat]:
                inflects.extend(paradigms[typ][spec_cat][form_str])
            if form[-1] != "N" and form_str[:-1] + "C" in paradigms[typ][spec_cat]:
                inflects.extend(paradigms[typ][spec_cat][form_str[:-1] + "C"])
            if form_str[:-1] + "X" in paradigms[typ][spec_cat]:
                inflects.extend(paradigms[typ][spec_cat][form_str[:-1] + "X"])
        if gen_cat in paradigms[typ]:
            if form_str in paradigms[typ][gen_cat]:
                inflects.extend(paradigms[typ][gen_cat][form_str])
            if form[-1] != "N" and form_str[:-1] + "C" in paradigms[typ][gen_cat]:
                inflects.extend(paradigms[typ][gen_cat][form_str[:-1] + "C"])
            if form_str[:-1] + "X" in paradigms[typ][gen_cat]:
                inflects.extend(paradigms[typ][gen_cat][form_str[:-1] + "X"])
    else:
        if spec_cat in paradigms[typ] and form_str in paradigms[typ][spec_cat]:
            inflects.extend(paradigms[typ][spec_cat][form_str])
        if gen_cat in paradigms[typ] and form_str in paradigms[typ][gen_cat]:
            inflects.extend(paradigms[typ][gen_cat][form_str])
    if len(inflects):
        inflects.sort(key=lambda infl: infl["props"][1])
        return inflects[0]["ending"]
    raise Exception()
