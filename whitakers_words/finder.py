from enum import Enum
from typing import Sequence, Union

from whitakers_words.datatypes import Inflect
from whitakers_words.enums import WordType
from whitakers_words.generated.paradigms import paradigms

partype = dict[str, dict[str, list[Inflect]]]
strs_or_ints = Sequence[Union[str, int]]


def find_inflection(wordType: Enum, n: strs_or_ints, form: strs_or_ints) -> str:
    typ = wordType.name
    inflects = find_inflects(paradigms[typ], n, form)
    if wordType == WordType.N or wordType == WordType.PRON:
        basic = list(form[:-1])
        if form[-1] != "N":
            inflects.extend(find_inflects(paradigms[typ], n, basic + ["C"]))
        inflects.extend(find_inflects(paradigms[typ], n, basic + ["X"]))
    elif wordType == WordType.ADJ or wordType == WordType.NUM:
        basic = list(form[:-2])
        if form[-2] != "N":
            inflects.extend(find_inflects(paradigms[typ], n, basic + ["C", form[-1]]))
        inflects.extend(find_inflects(paradigms[typ], n, basic + ["X", form[-1]]))
    if len(inflects):
        inflects.sort(key=lambda infl: infl["props"][1])
        return inflects[0]["ending"]
    raise Exception(form)


def find_inflects(para: partype, n: strs_or_ints, form: strs_or_ints) -> list[Inflect]:
    spec = 10 * int(n[0]) + int(n[1])
    spec_str = str(spec)
    gen_str = str(spec // 10 * 10)
    form_str = " ".join([str(x) for x in form]).upper()
    result = []
    if spec_str in para and form_str in para[spec_str]:
        result.extend(para[spec_str][form_str])
    if gen_str in para and form_str in para[gen_str]:
        result.extend(para[gen_str][form_str])
    if "0" in para and form_str in para["0"]:
        result.extend(para["0"][form_str])
    return result
