from typing import Sequence, TypedDict, Union


class Stem(TypedDict):
    orth: str
    pos: str
    form: Sequence[Union[str, int]]
    n: Sequence[int]
    wid: int
    props: list[str]
    stem_number: int


class Inflect(TypedDict):
    ending: str
    pos: str
    form: Sequence[str]
    n: Sequence[int]
    note: str
    props: Sequence[str]
    iid: int
    stem: int


class Unique(TypedDict, total=False):
    orth: str
    pos: str
    form: Sequence[str]
    senses: Sequence[str]
    n: Sequence[int]
    props: list[str]


class DictEntry(TypedDict, total=False):
    id: int
    orth: str
    parts: Sequence[str]
    pos: str
    form: Sequence[Union[int, str]]
    n: Sequence[int]
    senses: Sequence[str]


class Addon(TypedDict, total=False):
    orth: str
    pos: str
    senses: Sequence[str]
    form: str
    aid: int
