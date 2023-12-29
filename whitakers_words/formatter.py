import json
from enum import Enum
from typing import Any

import yaml

from whitakers_words.enums import WordType
from whitakers_words.finder import find_infl

from .parser import Analysis, UniqueLexeme, Word
from .util import make_ordinal

immutables = [WordType.CONJ, WordType.INTERJ, WordType.PREP]
genders = ["M", "F", "N"]


class Formatter:
    def format_result(self, word: Word) -> str:
        raise NotImplementedError("needs to be subclassed")


class YamlFormatter(Formatter):
    class _NoAliasNoTagDumper(yaml.Dumper):
        """
        From https://github.com/progala/ttl255.com/blob/master/yaml/anchors-and-aliases/yaml_same_ids_custom_dumper.py
        Licensed under MIT license
        """

        def ignore_aliases(self, data: Any) -> bool:
            return True

        def process_tag(self) -> None:
            pass

    def format_result(self, word: Word) -> str:
        result = yaml.dump(word, Dumper=YamlFormatter._NoAliasNoTagDumper)
        return result


class JsonFormatter(Formatter):
    class _CustomJsonEncoder(json.JSONEncoder):
        def default(self, ref: Any) -> Any:
            if isinstance(ref, Enum):
                return ref.value
            return ref.__dict__

    def format_result(self, word: Word) -> str:
        return json.dumps(word, indent=4, cls=JsonFormatter._CustomJsonEncoder)


class WordsFormatter(Formatter):
    def format_result(self, word: Word) -> str:
        result = ""
        for form in word.forms:
            if form.enclitic:
                result += form.enclitic.text
                result += " " * (21 - len(form.enclitic.text))
                result += "TACKON\n"
                result += "; ".join(sense for sense in form.enclitic.senses)
            for analysis in form.analyses.values():
                result += "\n"
                for inflection in analysis.inflections:
                    result += inflection.stem
                    if inflection.affix:
                        result += f".{inflection.affix}"
                    result += " " * (21 - (len(form.text) + 1))
                    result += inflection.wordType.name
                    result += " " * (7 - len(inflection.wordType.name))
                    result += " ".join(str(i) for i in inflection.category)
                    result += " "
                    result += " ".join(
                        feat.name for feat in inflection.features.values()
                    )
                    result += "\n"
                props = "".join(analysis.lexeme.props)
                result += f"{self.format_parts(analysis)}   [{props}]\n"
                result += "; ".join(sense for sense in analysis.lexeme.senses)
        return result

    def format_parts(self, analysis: Analysis) -> str:
        if isinstance(analysis.lexeme, UniqueLexeme):
            # TODO get meaningful output, esp. for forms of esse
            return ""
        if analysis.lexeme.wordType in immutables:
            return f"{analysis.lexeme.roots[0]}  {analysis.lexeme.wordType.name}"
        if analysis.lexeme.wordType == WordType.N:
            return format_noun(analysis)
        if analysis.lexeme.wordType == WordType.V:
            return format_verb(analysis)
        if analysis.lexeme.wordType == WordType.ADJ:
            return format_adj(analysis)
        return ""


def format_noun(analysis: Analysis) -> str:
    lex = analysis.lexeme
    root = lex.roots
    category = int(lex.category[0])
    gender = lex.form[0]
    nom = find_infl(WordType.N, lex.category, ["NOM", "S", gender])
    gen = find_infl(WordType.N, lex.category, ["GEN", "S", gender])
    gen_str = f", {root[1]}{gen}" if len(root) > 1 else "   "
    return f"{root[0]}{nom}{gen_str}  N ({make_ordinal(category)}) {gender}"


def format_verb(analysis: Analysis) -> str:
    lex = analysis.lexeme
    root = lex.roots
    category = int(lex.category[0])
    try:
        ind = find_infl(WordType.V, lex.category, ["PRES", "ACTIVE", "IND", "1", "S"])
        inf = find_infl(WordType.V, lex.category, ["PRES", "ACTIVE", "INF", "0", "X"])
        perf = find_infl(WordType.V, lex.category, ["PERF", "ACTIVE", "IND", "1", "S"])
        part = find_infl(WordType.VPAR, lex.category, ["NOM", "S", "M", "PERF", "PASSIVE"])
        return f"{root[0]}{ind}, {root[1]}{inf}, {root[2]}{perf}, {root[3]}{part}  V ({make_ordinal(category)}) "
    except Exception:
        # especially for edo
        return ""


def format_adj(analysis: Analysis) -> str:
    lex = analysis.lexeme
    root = lex.roots
    pos = [
        find_infl(WordType.ADJ, lex.category, ["NOM", "S", x, "POS"]) for x in genders
    ]
    comp = [
        find_infl(WordType.ADJ, lex.category, ["NOM", "S", x, "COMP"]) for x in genders
    ]
    sup = [
        find_infl(WordType.ADJ, lex.category, ["NOM", "S", x, "SUPER"]) for x in genders
    ]
    pos_str = f"{root[0]}{pos[0]}, {root[1]}{pos[1]} -{pos[2]}"
    comp_str = sup_str = "  "
    if len(root) > 2:
        comp_str = f", {root[2]}{comp[0]} -{comp[1]} -{comp[2]}"
        if len(root) > 3:
            sup_str = f", {root[3]}{sup[0]} -{sup[1]} -{sup[2]}"
    return f"{pos_str}{comp_str}{sup_str}  ADJ"
