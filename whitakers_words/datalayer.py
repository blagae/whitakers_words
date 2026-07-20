import json
import os
import sqlite3
import threading
from typing import Any, Optional, Sequence, Tuple

from .datatypes import Addon, DictEntry, Inflect, Stem, Unique
from .util import canonicalize_orth


def default_database_path() -> str:
    return os.path.join(os.path.dirname(__file__), "generated", "words.db")


class DataLayer:
    def __new__(cls, **kwargs: Any) -> "DataLayer":
        database = kwargs.get("database")
        if isinstance(database, str) and database.startswith("mysql://"):
            return super().__new__(MySqlDataLayer)
        if database:
            return super().__new__(SqliteDataLayer)
        return super().__new__(FileBasedDataLayer)

    def __init__(self, **kwargs: Any):
        if "addons" in kwargs:
            addons: dict[str, Sequence[Addon]] = kwargs["addons"]
        else:
            from .data.addons import addons  # type: ignore[no-redef]
        # addons are spelled in Whitaker's j/v orthography ("ve"), queries in canonical i/u
        self.addons: dict[str, Sequence[Addon]] = {
            addon_type: [dict(addon, orth=canonicalize_orth(addon["orth"]))  # type: ignore[misc]
                         if "orth" in addon else addon
                         for addon in addon_list]
            for addon_type, addon_list in addons.items()
        }

        self.age: str = kwargs.get("age", "C")
        self.area: str = kwargs.get("area", "A")
        self.geo: str = kwargs.get("geo", "A")
        self.frequency: str = kwargs.get("frequency", "C")
        self.inflection_frequency: str = kwargs.get("frequency", "B")
        self.source: str = kwargs.get("source", "A")

    def find_enclitic(self, text: str, addon_type: str) -> list[Tuple[str, Addon]]:
        result = []
        if addon_type in self.addons:
            for affix in self.addons[addon_type]:
                affix_text = affix["orth"]
                if affix_text and text.endswith(affix_text):
                    base = text[: -len(affix_text)]
                    # an enclitic without a base is not an enclitic
                    if base:
                        result.append((base, affix))
        return result

    def get_frequency(self) -> str:
        return self.frequency

    def get_uniques(self, text: str) -> Sequence[Unique]:
        raise NotImplementedError()

    def get_empty_inflections(self, text: str) -> list[Inflect]:
        raise NotImplementedError()

    def get_inflections(self, text: str) -> list[Inflect]:
        raise NotImplementedError()

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        raise NotImplementedError()

    def get_stems(self, text: str) -> Sequence[Stem]:
        raise NotImplementedError()


class FileBasedDataLayer(DataLayer):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        if "wordlist" in kwargs:
            self.wordlist: Sequence[DictEntry] = kwargs["wordlist"]
        else:
            from .generated.wordlist import wordlist

            self.wordlist = wordlist
        # input may be a set or a list
        if "wordkeys" in kwargs:
            self.wordkeys: set[str] = set(kwargs["wordkeys"])
        else:
            from .generated.wordkeys import wordkeys

            self.wordkeys = set(wordkeys)
        if "stems" in kwargs:
            self.stems: dict[str, Sequence[Stem]] = kwargs["stems"]
        else:
            from .generated.stems import stems

            self.stems = stems
        if "uniques" in kwargs:
            self.uniques: dict[str, Sequence[Unique]] = kwargs["uniques"]
        else:
            from .generated.uniques import uniques

            self.uniques = uniques
        if "inflects" in kwargs:
            self.inflects: dict[str, dict[str, Sequence[Inflect]]] = kwargs["inflects"]
        else:
            from .generated.inflects import inflects

            self.inflects = inflects
        if "empty" in kwargs:
            self.empty: dict[str, Sequence[Inflect]] = kwargs["empty"]
        else:
            from .generated.empty import empty

            self.empty = empty
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
        return any(x["props"][3] <= self.frequency for x in item[1])

    def get_uniques(self, text: str) -> Sequence[Unique]:
        return self.uniques.get(text, [])

    def get_empty_inflections(self, text: str) -> list[Inflect]:
        result: list[Inflect] = []
        if text in self.wordkeys and text in self.stems:
            stem_list = self.stems[text]
            wordtypes = {x["pos"] for x in stem_list}
            # no need to check for VPAR, because there are no empty VPAR endings
            for wordtype in wordtypes:
                result.extend(self.empty[wordtype])
        return result

    def get_inflections(self, text: str) -> list[Inflect]:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        result = self.get_empty_inflections(text)
        # Check against inflection list
        for inflect_length in range(1, min(8, len(text))):
            ending_list = self.inflects.get(str(inflect_length))
            if ending_list:
                infl = ending_list.get(text[-inflect_length:])
                if infl:
                    result.extend(infl)
        return result

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        return self.wordlist[id]

    def get_stems(self, text: str) -> Sequence[Stem]:
        return self.stems.get(text, [])


class SqliteDataLayer(DataLayer):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        database = kwargs["database"]
        path = database if isinstance(database, str) else default_database_path()
        if not os.path.exists(path):
            from .datagenerator import generate_database

            generate_database(path)
        self.conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        # the empty inflections are a handful of rows, so keep them in memory
        self.empty: dict[str, Sequence[Inflect]] = {
            pos: json.loads(data)
            for pos, data in self.conn.execute("SELECT pos, data FROM empty")
        }

    def get_uniques(self, text: str) -> Sequence[Unique]:
        rows = self.conn.execute("SELECT data FROM uniques WHERE orth = ?", (text,))
        return [json.loads(row[0]) for row in rows]

    def get_empty_inflections(self, text: str) -> list[Inflect]:
        result: list[Inflect] = []
        stem_list = self.get_stems(text)
        if stem_list and self._is_wordkey(text):
            wordtypes = {x["pos"] for x in stem_list}
            # no need to check for VPAR, because there are no empty VPAR endings
            for wordtype in wordtypes:
                result.extend(self.empty[wordtype])
        return result

    def get_inflections(self, text: str) -> list[Inflect]:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        result = self.get_empty_inflections(text)
        # an ending determines its own length, so all candidate endings can go in a single query
        endings = [text[-length:] for length in range(1, min(8, len(text)))]
        if endings:
            placeholders = ", ".join("?" * len(endings))
            rows = self.conn.execute(
                f"SELECT data FROM inflects WHERE ending IN ({placeholders})"
                " AND freq <= ? AND (age <= ? OR age = 'X') ORDER BY length, rowid",
                (*endings, self.inflection_frequency, self.age),
            )
            result.extend(json.loads(row[0]) for row in rows)
        return result

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        row = self.conn.execute(
            "SELECT data FROM wordlist WHERE id = ?", (id,)
        ).fetchone()
        return json.loads(row[0]) if row else None

    def get_stems(self, text: str) -> Sequence[Stem]:
        rows = self.conn.execute(
            "SELECT freq, data FROM stems WHERE orth = ? ORDER BY rowid", (text,)
        ).fetchall()
        # keep the whole group if any of its stems is frequent enough,
        # mirroring FileBasedDataLayer._filter_stems
        if any(freq <= self.frequency for freq, _ in rows):
            return [json.loads(data) for _, data in rows]
        return []

    def _is_wordkey(self, text: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM wordkeys WHERE orth = ?", (text,)
        ).fetchone()
        return row is not None


class MySqlDataLayer(DataLayer):
    """
    Reads the ww_* tables written by datagenerator.dump_mysql_database, typically
    in a database shared with a consuming application. Construct with
    database="mysql://user:password@host:port/dbname" (requires the [mysql] extra).

    A single pymysql connection is not safe for concurrent use from multiple
    threads (interleaved queries corrupt its protocol state), but ONE
    instance of this layer commonly IS shared across threads: elisio caches
    one module-level default Parser (elisio.word._get_default_parser),
    which a threaded ASGI server's threadpool then calls from a different
    worker thread per request. So each thread lazily opens and keeps its
    OWN connection, in thread-local storage, transparent to callers.
    ORDER BY id reproduces the sqlite layer's rowid ordering.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._database_url: str = kwargs["database"]
        self._local = threading.local()
        try:
            # the empty inflections are a handful of rows, so keep them in memory
            self.empty: dict[str, Sequence[Inflect]] = {
                pos: json.loads(data)
                for pos, data in self._fetchall("SELECT pos, data FROM ww_empty")
            }
        except Exception as exc:
            # unlike the sqlite layer we never auto-build: a shared server
            # database should not be rebuilt as an import side effect
            raise RuntimeError(
                "MySQL dictionary tables not found or unreadable; run"
                " whitakers_words.datagenerator.generate_mysql_database(url) first"
            ) from exc

    @property
    def conn(self) -> Any:
        connection = getattr(self._local, "conn", None)
        if connection is None:
            from .datagenerator import connect_mysql

            connection = connect_mysql(self._database_url)
            self._local.conn = connection
        return connection

    def _fetchall(self, query: str, args: Tuple[Any, ...] = ()) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
            return list(cursor.fetchall())

    def get_uniques(self, text: str) -> Sequence[Unique]:
        rows = self._fetchall(
            "SELECT data FROM ww_uniques WHERE orth = %s ORDER BY id", (text,)
        )
        return [json.loads(row[0]) for row in rows]

    def get_empty_inflections(self, text: str) -> list[Inflect]:
        result: list[Inflect] = []
        stem_list = self.get_stems(text)
        if stem_list and self._is_wordkey(text):
            wordtypes = {x["pos"] for x in stem_list}
            # no need to check for VPAR, because there are no empty VPAR endings
            for wordtype in wordtypes:
                result.extend(self.empty[wordtype])
        return result

    def get_inflections(self, text: str) -> list[Inflect]:
        """
        Find all possible endings that may apply, so without checking congruence between word type and ending type
        """
        # the word may be undeclined, so add this as an option if the full form exists in the list of words
        result = self.get_empty_inflections(text)
        # an ending determines its own length, so all candidate endings can go in a single query
        endings = [text[-length:] for length in range(1, min(8, len(text)))]
        if endings:
            placeholders = ", ".join(["%s"] * len(endings))
            rows = self._fetchall(
                f"SELECT data FROM ww_inflects WHERE ending IN ({placeholders})"
                " AND freq <= %s AND (age <= %s OR age = 'X') ORDER BY length, id",
                (*endings, self.inflection_frequency, self.age),
            )
            result.extend(json.loads(row[0]) for row in rows)
        return result

    def lookup_stem(self, id: int) -> Optional[DictEntry]:
        rows = self._fetchall("SELECT data FROM ww_wordlist WHERE id = %s", (id,))
        return json.loads(rows[0][0]) if rows else None

    def get_stems(self, text: str) -> Sequence[Stem]:
        rows = self._fetchall(
            "SELECT freq, data FROM ww_stems WHERE orth = %s ORDER BY id", (text,)
        )
        # keep the whole group if any of its stems is frequent enough,
        # mirroring FileBasedDataLayer._filter_stems
        if any(freq <= self.frequency for freq, _ in rows):
            return [json.loads(data) for _, data in rows]
        return []

    def _is_wordkey(self, text: str) -> bool:
        return bool(self._fetchall("SELECT 1 FROM ww_wordkeys WHERE orth = %s", (text,)))
