from enum import Enum
from typing import Sequence, Union

from whitakers_words.datatypes import Inflect
from whitakers_words.enums import WordType
from whitakers_words.generated.paradigms import paradigms

partype = dict[str, dict[str, list[Inflect]]]
strs_or_ints = Sequence[Union[str, int]]


def find_infl(wordType: Enum, n: strs_or_ints, form: strs_or_ints) -> str:
    typ = wordType.name
    inflects = get_candidates(paradigms[typ], n, form)
    if wordType == WordType.N or wordType == WordType.PRON:
        basic = list(form[:-1])
        if form[-1] != "N":
            inflects.extend(get_candidates(paradigms[typ], n, basic + ["C"]))
        inflects.extend(get_candidates(paradigms[typ], n, basic + ["X"]))
    elif wordType == WordType.ADJ or wordType == WordType.NUM:
        basic = list(form[:-2])
        if form[-2] != "N":
            inflects.extend(get_candidates(paradigms[typ], n, basic + ["C", form[-1]]))
        inflects.extend(get_candidates(paradigms[typ], n, basic + ["X", form[-1]]))
    if len(inflects):
        inflects.sort(key=lambda infl: infl["props"][1])
        return inflects[0]["ending"]
    raise Exception(form)


def get_candidates(par: partype, n: strs_or_ints, form: strs_or_ints) -> list[Inflect]:
    spec = 10 * int(n[0]) + int(n[1])
    spec_str = str(spec)
    gen_str = str(spec // 10 * 10)
    form_str = " ".join([str(x) for x in form]).upper()
    catchall_string = 'X X X'
    result = []
    if spec_str in par:
        if form_str in par[spec_str]:
            result.extend(par[spec_str][form_str])
        if catchall_string in par[spec_str]:
            result.extend(par[spec_str][catchall_string])
    if gen_str in par:
        if form_str in par[gen_str]:
            result.extend(par[gen_str][form_str])
        if catchall_string in par[gen_str]:
            result.extend(par[gen_str][catchall_string])
    if "0" in par and form_str in par["0"]:
        result.extend(par["0"][form_str])
    return result
