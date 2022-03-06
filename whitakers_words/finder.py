from whitakers_words.datatypes import Inflect
from whitakers_words.enums import WordType
from whitakers_words.generated.paradigms import paradigms


# TODO heavy refactoring
def find_inflection(wordType: WordType, n: list[int], form: list[str]) -> str:
    num = str(10 * n[0] + n[1])
    ff = " ".join(form).upper()
    typ = wordType.name
    if wordType == WordType.N:
        inflects = []
        if num in paradigms[typ]:
            if ff in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff])
            if form[-1] != "N" and ff[:-1] + "C" in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff[:-1] + "C"])
            if ff[:-1] + "X" in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff[:-1] + "X"])
        else:
            num = str(10 * n[0])
            if ff in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff])
            if form[-1] != "N" and ff[:-1] + "C" in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff[:-1] + "C"])
            if ff[:-1] + "X" in paradigms[typ][num]:
                inflects.extend(paradigms[typ][num][ff[:-1] + "X"])
    else:
        if num not in paradigms[typ] or ff not in paradigms[typ][num]:
            num = str(10 * n[0])
        if num not in paradigms[typ] or ff not in paradigms[typ][num]:
            raise Exception()
        inflects: list[Inflect] = paradigms[typ][num][ff]
    if len(inflects):
        inflects.sort(key = lambda infl: infl["props"][1])
        return inflects[0]["ending"]
    raise Exception()