from enum import Enum
from typing import Sequence, Union
from whitakers_words.datatypes import Inflect
from whitakers_words.enums import WordType
from whitakers_words.generated.paradigms import paradigms


partype = type(paradigms["V"])
strs_or_ints = type(Sequence[Union[str, int]])


def find_inflection(wordType: Enum, n: strs_or_ints, form: strs_or_ints) -> str:
    spec_cat = 10 * int(n[0]) + int(n[1])
    form_str = " ".join([str(x) for x in form]).upper()
    typ = wordType.name
    inflects = find_inflects(paradigms[typ], spec_cat, form_str)
    if wordType == WordType.N:
        ungendered = form_str[:-1]
        if form[-1] != "N":
            inflects.extend(find_inflects(paradigms[typ], spec_cat, ungendered + "C"))
        inflects.extend(find_inflects(paradigms[typ], spec_cat, ungendered + "X"))
    if len(inflects):
        inflects.sort(key=lambda infl: infl["props"][1])
        return inflects[0]["ending"]
    raise Exception()


def find_inflects(para: partype, spec: int, form: str) -> list[Inflect]:
    spec_str = str(spec)
    gen_str = str(spec // 10 * 10)
    result = []
    if spec_str in para and form in para[spec_str]:
        result.extend(para[spec_str][form])
    if gen_str in para and form in para[gen_str]:
        result.extend(para[gen_str][form])
    return result
