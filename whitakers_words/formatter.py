import json
from enum import Enum
from typing import Any

import yaml

from whitakers_words.enums import WordType
from whitakers_words.finder import find_inflection

from .parser import Analysis, Word
from .util import make_ordinal


class Formatter:
    def format_result(self, word: Word) -> str:
        raise NotImplementedError("needs to be subclassed")


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
                    result += f"{inflection.stem}.{inflection.affix}"
                    result += " " * (21 - (len(form.text) + 1))
                    result += inflection.wordType.name
                    result += " " * (7 - len(inflection.wordType.name))
                    result += " ".join(str(i) for i in inflection.category)
                    result += " "
                    result += " ".join(
                        feat.name for feat in inflection.features.values()
                    )
                    result += "\n"
                props = ''.join(analysis.lexeme.props)
                result += f"{self.format_parts(analysis)}   [{props}]\n"
                result += "; ".join(sense for sense in analysis.lexeme.senses)
        return result

    def format_parts(self, analysis: Analysis) -> str:
        if analysis.lexeme.wordType == WordType.N:
            return self.format_noun(analysis)
        return ''

    def format_noun(self, analysis: Analysis) -> str:
        lex = analysis.lexeme
        root = lex.roots
        category = int(lex.category[0])
        gender = lex.form[0]
        nom = find_inflection(lex.wordType, lex.category, ["NOM", "S", gender])
        gen = find_inflection(lex.wordType, lex.category, ["GEN", "S", gender])
        return f"{root[0]}{nom}, {root[1]}{gen}  N ({make_ordinal(category)}) {gender}"


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
