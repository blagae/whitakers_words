from typing import Any, Sequence, Tuple

from .data.addons import addons
from .datatypes import Addon, DictEntry, Inflect, Stem, Unique
from .generated.empty import empty
from .generated.inflects import inflects
from .generated.stems import stems
from .generated.uniques import uniques
from .generated.wordkeys import wordkeys
from .generated.wordlist import wordlist


class DataLayer:

    def __init__(self, **kwargs: Any):
        self.wordlist: Sequence[DictEntry] = kwargs.get('wordlist', wordlist)
        self.wordkeys: set[str] = set(kwargs.get('wordkeys', wordkeys))  # input may be a set or a list
        self.stems: dict[str, Sequence[Stem]] = kwargs.get('stems', stems)
        self.uniques: dict[str, Sequence[Unique]] = kwargs.get('uniques', uniques)
        self.inflects: dict[str, dict[str, Sequence[Inflect]]] = kwargs.get('inflects', inflects)
        self.addons: dict[str, Sequence[Addon]] = kwargs.get('addons', addons)
        self.empty: dict[str, Sequence[Inflect]] = kwargs.get('empty', empty)

        self.age: str = kwargs.get('age', "A")
        self.area: str = kwargs.get('area', "A")
        self.geo: str = kwargs.get('geo', "A")
        self.frequency: str = kwargs.get('frequency', "C")
        self.source: str = kwargs.get('source', "A")
        self.create_subsets()

    def create_subsets(self) -> None:
        self.stems = dict(filter(self.filter_stems, self.stems.items()))
        result: dict[str, dict[str, Sequence[Inflect]]] = {}
        for length_index, ending_list in self.inflects.items():
            result[length_index] = {}
            for text, definition in ending_list.items():
                lst = list(filter(self.filter_inflections, definition))
                if lst:
                    result[length_index][text] = lst
        self.inflects = result

    def filter_inflections(self, item: Inflect) -> bool:
        # TODO use all filters: [AGE, FREQ]
        return item["props"][1] <= 'B'  # TODO make configurable again

    def filter_stems(self, item: Tuple[str, Sequence[Stem]]) -> bool:
        # TODO use all filters: [AGE, AREA, GEO, FREQ, SOURCE]
        return bool(list(filter(lambda x: x["props"][3] <= self.frequency, item[1])))
