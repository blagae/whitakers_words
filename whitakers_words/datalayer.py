import re
from typing import Any, Optional, Sequence, Tuple

from .data.addons import addons
from .datatypes import Addon, DictEntry, Inflect, Stem, Unique
from .generated.empty import empty
from .generated.inflects import inflects
from .generated.stems import stems
from .generated.uniques import uniques
from .generated.wordkeys import wordkeys
from .generated.wordlist import wordlist


class DataLayer:
    def __new__(cls, **kwargs):
        if "database" in kwargs:
            # TODO allow database implementations
            raise NotImplementedError()
        return super().__new__(FileBasedDataLayer)

    def find_enclitic(self, text: str, addon_type: str) -> list[dict[str, str]]:
        raise NotImplementedError()

    def get_frequency(self):
        raise NotImplementedError()

    def get_uniques(self, text: str) -> Sequence[Unique]:
        raise NotImplementedError()

    def get_empty_inflections(self, text: str) -> Sequence[Inflect]:
        raise NotImplementedError()

    def get_inflections(self, text: str) -> Sequence[Inflect]:
        raise NotImplementedError()

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        raise NotImplementedError()

    def get_stems(self, text: str):
        raise NotImplementedError()


class FileBasedDataLayer(DataLayer):
    def __init__(self, **kwargs: Any):
        self.wordlist: Sequence[DictEntry] = kwargs.get("wordlist", wordlist)
        # input may be a set or a list
        self.wordkeys: set[str] = set(kwargs.get("wordkeys", wordkeys))
        self.stems: dict[str, Sequence[Stem]] = kwargs.get("stems", stems)
        self.uniques: dict[str, Sequence[Unique]] = kwargs.get("uniques", uniques)
        self.inflects: dict[str, dict[str, Sequence[Inflect]]] = kwargs.get(
            "inflects", inflects
        )
        self.addons: dict[str, Sequence[Addon]] = kwargs.get("addons", addons)
        self.empty: dict[str, Sequence[Inflect]] = kwargs.get("empty", empty)

        self.age: str = kwargs.get("age", "C")
        self.area: str = kwargs.get("area", "A")
        self.geo: str = kwargs.get("geo", "A")
        self.frequency: str = kwargs.get("frequency", "C")
        self.inflection_frequency: str = kwargs.get("frequency", "B")
        self.source: str = kwargs.get("source", "A")
        self._create_subsets()

    def _create_subsets(self) -> None:
        self.stems = dict(filter(self._filter_stems, self.stems.items()))
        result: dict[str, dict[str, Sequence[Inflect]]] = {}
        for length_index, ending_list in self.inflects.items():
            result[length_index] = {}
            for text, definition in ending_list.items():
                lst = list(filter(self._filter_inflections, definition))
                if lst:
                    result[length_index][text] = lst
        self.inflects = result

    def _filter_inflections(self, item: Inflect) -> bool:
        return item["props"][1] <= self.inflection_frequency and (
            item["props"][0] <= self.age or item["props"][0] == "X"
        )

    def _filter_stems(self, item: Tuple[str, Sequence[Stem]]) -> bool:
        # TODO use all filters: [AGE, AREA, GEO, FREQ, SOURCE]
        return bool(list(filter(lambda x: x["props"][3] <= self.frequency, item[1])))

    # INTERFACE STARTS HERE
    def find_enclitic(self, text: str, addon_type: str) -> list[dict[str, str]]:
        result = []
        if addon_type in self.addons:
            for affix in self.addons[addon_type]:
                affix_text = affix["orth"]
                if text.endswith(affix_text):
                    base = re.sub(affix_text + "$", "", text)
                    # an enclitic without a base is not an enclitic
                    if base:
                        result.append({"base": base, "affix": affix})
        return result

    def get_frequency(self):
        return self.frequency

    def get_uniques(self, text: str) -> Sequence[Unique]:
        return self.uniques.get(text, [])

    def get_empty_inflections(self, text: str) -> Sequence[Inflect]:
        result = []
        if text in self.wordkeys and text in self.stems:
            stem_list = self.stems[text]
            wordtypes = {x["pos"] for x in stem_list}
            # no need to check for VPAR, because there are no empty VPAR endings
            for wordtype in wordtypes:
                result.extend(self.empty[wordtype])
        return result

    def get_inflections(self, text: str) -> Sequence[Inflect]:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        result: list[Inflect] = self.get_empty_inflections(text)
        # Check against inflection list
        for inflect_length in range(1, min(8, len(text))):
            end_of_word = text[-inflect_length:]
            if (
                str(inflect_length) in self.inflects
                and end_of_word in self.inflects[str(inflect_length)]
            ):
                infl = self.inflects[str(inflect_length)][end_of_word]
                result.extend(infl)
        return result

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        return self.wordlist[id]

    def get_stems(self, text: str):
        return self.stems.get(text, [])
