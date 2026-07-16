"""
datagenerator.py

Format the data from the input files from Whitaker's Words into python dictionaries
and an equivalent sqlite or MySQL database
"""
import json
import os
import sqlite3
from typing import Any, Iterable, Iterator, Mapping, Optional, Sequence, Tuple, Union
from urllib.parse import unquote, urlsplit

from .datatypes import DictEntry, Inflect, Stem, Unique
from .util import canonicalize_orth


class Generator:
    def __init__(self) -> None:
        self.resources = os.path.join(os.path.dirname(__file__), "data")
        self.filedir = os.path.join(os.path.dirname(__file__), "generated") + os.sep
        try:
            os.mkdir(self.filedir)
        except FileExistsError:
            pass

    def dump_file(
        self, name: str, obj: Any = None, definition: str = "", imports: str = ""
    ) -> None:
        with open(self.filedir + name, "w") as out:
            if obj:
                if "Sequence" in definition:
                    out.write("from typing import Sequence\n\n")
                if imports:
                    out.write(f"from ..datatypes import {imports}\n\n")
                local_def = f": {definition}" if definition else ""
                out.write(f"{name[:-3]}{local_def} = ")
                json.dump(obj, out)
            out.write("\n")

    def import_dicts(
        self,
    ) -> Tuple[Sequence[str], Sequence[DictEntry], dict[str, Sequence[Stem]]]:
        keys: Sequence[str] = list()
        ids: Sequence[DictEntry] = [{}]
        stems: dict[str, Sequence[Stem]] = dict()
        previous_item: DictEntry = {}

        parts_slicer = slice(None, 76)
        pos_slicer = slice(76, 83)
        form_slicer = slice(83, 100)
        properties_slicer = slice(100, 110)
        sense_slicer = slice(109, None)

        with open(self.resources + "/DICTLINE.GEN", encoding="ISO-8859-1") as f:
            for i, line in enumerate(f):

                parts = line[parts_slicer].replace("zzz", "-").split()
                parts = [canonicalize_orth(x.lower()) for x in parts]
                orth = parts[0]
                pos = line[pos_slicer].strip()
                raw_form = line[form_slicer].strip()
                properties = line[properties_slicer].split()
                n: Sequence[int] = []
                form: Sequence[Union[str, int]] = []
                for v in raw_form.split():
                    try:
                        val = int(v)
                        if len(n) >= 2:
                            form.append(val)
                        else:
                            n.append(val)
                    except ValueError:
                        form.append(v)

                senses = [
                    sense.strip()
                    for sense in line[sense_slicer].strip().split(";")
                    if sense
                ]

                item: DictEntry = {
                    "id": i + 1,
                    "orth": orth,
                    "parts": parts,
                    "pos": pos,
                    "form": form,
                    "n": n,
                    "senses": senses,
                }
                for stem_number, part in enumerate(parts):
                    stem: Stem = {
                        "orth": part,
                        "pos": pos,
                        "form": form,
                        "n": n,
                        "wid": i + 1,
                        "props": properties,
                        "stem_number": stem_number,
                    }
                    if part in stems:
                        stems[part].append(stem)
                    else:
                        stems[part] = [stem]
                # contracted -ivi perfects (iit, petiit, abiisse, audierat):
                # a perfect stem in -iu (= -iv) also occurs without the u
                # before its endings, which all start with i or e
                if pos == "V" and len(parts) > 2 and parts[2].endswith("iu"):
                    contracted: Stem = {
                        "orth": parts[2][:-1],
                        "pos": pos,
                        "form": form,
                        "n": n,
                        "wid": i + 1,
                        "props": properties,
                        "stem_number": 2,
                    }
                    if contracted["orth"] in stems:
                        stems[contracted["orth"]].append(contracted)
                    else:
                        stems[contracted["orth"]] = [contracted]
                if senses[0].startswith("|"):
                    senses[0] = senses[0].replace("|", "")
                    previous_item["senses"].extend(senses)
                    ids.append(dict())
                else:
                    keys.extend(parts)
                    ids.append(item)
                    previous_item = item

        self.dump_file("wordkeys.py", keys, "list[str]")
        self.dump_file("wordlist.py", ids, "Sequence[DictEntry]", "DictEntry")
        self.dump_file("stems.py", stems, "dict[str, Sequence[Stem]]", "Stem")
        return keys, ids, stems

    def import_affixes(self) -> None:
        for affix in ["prefix", "suffix"]:
            with open(f"{self.resources}/{affix}es.txt") as f:

                counter = 0
                obj: Unique = {}
                data: Sequence[Unique] = []

                for line in f:
                    if counter == 0:
                        obj["orth"] = line.replace(affix.upper(), "").strip()

                    elif counter == 1:
                        split_line = line.strip().split()
                        obj["pos"] = split_line[0]
                        obj["form"] = split_line

                    elif counter == 2:
                        obj["senses"] = line.strip().split()

                    counter += 1
                    if counter == 3:
                        data.append(obj)
                        obj = {}
                        counter = 0

            self.dump_file(f"{affix}es.py", data)

    def import_uniques(self) -> dict[str, Sequence[Unique]]:
        with open(self.resources + "/UNIQUES.LAT") as f:

            counter = 0
            obj: Unique = {}
            data: dict[str, Sequence[Unique]] = dict()
            for line in f:
                if counter == 0:
                    obj["orth"] = canonicalize_orth(line.strip().lower())

                elif counter == 1:
                    contents = line.split()
                    obj["pos"] = contents[0]
                    obj["n"] = [int(x) for x in contents[1:3]]
                    obj["form"] = contents[3:-5]

                elif counter == 2:
                    obj["senses"] = line.strip().split()

                counter += 1
                if counter == 3:
                    orth = obj["orth"]
                    if orth in data:
                        data[orth].append(obj)
                    else:
                        data[orth] = [obj]
                    obj = {}
                    counter = 0

        from .data.esse import esse

        for est in esse:
            orth = est["orth"]
            est["n"] = [5, 1]
            est["props"] = ["X", "X", "X", "A", "X"]
            if orth in data:
                data[orth].append(est)
            else:
                data[orth] = [est]

        self.dump_file("uniques.py", data, "dict[str, Sequence[Unique]]", "Unique")
        return data

    def import_inflects(
        self,
    ) -> Tuple[dict[str, list[Inflect]], dict[int, dict[str, Sequence[Inflect]]]]:
        with open(self.resources + "/INFLECTS.LAT") as f:
            data = []
            paradigms: dict[str, dict[str, dict[str, list[Inflect]]]] = {}
            for i, text in enumerate(f):
                line = text.strip()
                if not line or line.startswith("--"):
                    continue
                comment = ""

                if "--" in line:
                    comment = line[line.index("--") + 2:].strip()
                    line = line[: line.index("--")]
                info = line.split()

                ending = info[-3]
                used_stem = info[-5]
                if not ending.isalpha():
                    ending = ""
                    used_stem = info[-4]
                ending = canonicalize_orth(ending.lower())
                pos = info[0]
                n = info[1:3]
                properties = info[-2:]
                if pos == "ADV":
                    n = info[-4:-2]
                    form = [info[1]]
                elif pos in ("PREP", "CONJ", "INTERJ"):
                    n = info[-4:-2]
                    form = info[1:-2]
                elif pos in ("V", "VPAR"):
                    form = info[3:8]
                elif pos in ("ADJ", "NUM"):
                    form = info[3:7]
                elif pos in ("N", "SUPINE", "PRON"):
                    form = info[3:6]
                else:
                    raise Exception()
                numbers = [int(x) for x in n]
                entry: Inflect = {
                    "ending": ending,
                    "n": numbers,
                    "note": comment,
                    "pos": pos,
                    "form": form,
                    "props": properties,
                    "iid": i,
                    "stem": int(used_stem) - 1,  # go zero-based
                }
                data.append(entry)
                if len(n) > 1:
                    category = str(10 * numbers[0] + numbers[1])
                else:
                    category = "0"
                if pos not in paradigms:
                    paradigms[pos] = {}
                if category not in paradigms[pos]:
                    paradigms[pos][category] = {}
                form_str = " ".join(form).upper()
                if form_str not in paradigms[pos][category]:
                    paradigms[pos][category][form_str] = []
                paradigms[pos][category][form_str].append(entry)
        empty, reordered = self.reorder_inflects(data)
        self.dump_file("empty.py", empty, "dict[str, Sequence[Inflect]]", "Inflect")
        self.dump_file(
            "inflects.py",
            reordered,
            "dict[str, dict[str, Sequence[Inflect]]]",
            "Inflect",
        )
        self.dump_file(
            "paradigms.py",
            paradigms,
            "dict[str, dict[str, dict[str, list[Inflect]]]]",
            "Inflect",
        )
        return empty, reordered

    def reorder_inflects(
        self, data: list[Inflect]
    ) -> Tuple[dict[str, list[Inflect]], dict[int, dict[str, Sequence[Inflect]]]]:
        # assuming all endings are at most 7 characters long
        keys = (x for x in range(1, 8))
        empty: dict[str, list[Inflect]] = {}
        result: dict[int, dict[str, Sequence[Inflect]]] = {key: dict() for key in keys}
        for item in data:
            if item["ending"]:
                end = item["ending"]
                store = result[len(end)]
                if end in store:
                    store[end].append(item)
                else:
                    store[end] = [item]
            else:
                pos = item["pos"]
                if pos in empty:
                    empty[pos].append(item)
                else:
                    empty[pos] = [item]
                pass
        return empty, result

    def create_init_file(self) -> None:
        self.dump_file("__init__.py")


def _wordlist_rows(wordlist: Sequence[DictEntry]) -> Iterator[Tuple[Any, ...]]:
    return ((i, json.dumps(entry)) for i, entry in enumerate(wordlist))


def _wordkeys_rows(wordkeys: Sequence[str]) -> Iterator[Tuple[Any, ...]]:
    return ((key,) for key in set(wordkeys))


def _stems_rows(stems: Mapping[str, Sequence[Stem]]) -> Iterator[Tuple[Any, ...]]:
    return (
        (orth, stem["props"][3], json.dumps(stem))
        for orth, stem_list in stems.items()
        for stem in stem_list
    )


def _uniques_rows(uniques: Mapping[str, Sequence[Unique]]) -> Iterator[Tuple[Any, ...]]:
    return (
        (orth, json.dumps(unique))
        for orth, unique_list in uniques.items()
        for unique in unique_list
    )


def _inflects_rows(
    inflects: Mapping[Any, Mapping[str, Sequence[Inflect]]]
) -> Iterator[Tuple[Any, ...]]:
    return (
        (int(length), ending, infl["props"][0], infl["props"][1], json.dumps(infl))
        for length, ending_list in inflects.items()
        for ending, infl_list in ending_list.items()
        for infl in infl_list
    )


def _empty_rows(empty: Mapping[str, Sequence[Inflect]]) -> Iterator[Tuple[Any, ...]]:
    return ((pos, json.dumps(infl_list)) for pos, infl_list in empty.items())


def dump_database(
    path: str,
    wordkeys: Sequence[str],
    wordlist: Sequence[DictEntry],
    stems: Mapping[str, Sequence[Stem]],
    uniques: Mapping[str, Sequence[Unique]],
    inflects: Mapping[Any, Mapping[str, Sequence[Inflect]]],
    empty: Mapping[str, Sequence[Inflect]],
) -> None:
    """
    Write the parsed data to a sqlite database, as an alternative to the generated
    python modules that is much cheaper to open at runtime
    """
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA journal_mode = OFF")
        conn.execute("CREATE TABLE wordlist (id INTEGER PRIMARY KEY, data TEXT NOT NULL)")
        conn.execute("CREATE TABLE wordkeys (orth TEXT PRIMARY KEY) WITHOUT ROWID")
        conn.execute("CREATE TABLE stems (orth TEXT NOT NULL, freq TEXT NOT NULL, data TEXT NOT NULL)")
        conn.execute("CREATE TABLE uniques (orth TEXT NOT NULL, data TEXT NOT NULL)")
        conn.execute(
            "CREATE TABLE inflects (length INTEGER NOT NULL, ending TEXT NOT NULL,"
            " age TEXT NOT NULL, freq TEXT NOT NULL, data TEXT NOT NULL)"
        )
        conn.execute("CREATE TABLE empty (pos TEXT PRIMARY KEY, data TEXT NOT NULL) WITHOUT ROWID")

        conn.executemany("INSERT INTO wordlist VALUES (?, ?)", _wordlist_rows(wordlist))
        conn.executemany("INSERT INTO wordkeys VALUES (?)", _wordkeys_rows(wordkeys))
        conn.executemany("INSERT INTO stems VALUES (?, ?, ?)", _stems_rows(stems))
        conn.executemany("INSERT INTO uniques VALUES (?, ?)", _uniques_rows(uniques))
        conn.executemany("INSERT INTO inflects VALUES (?, ?, ?, ?, ?)", _inflects_rows(inflects))
        conn.executemany("INSERT INTO empty VALUES (?, ?)", _empty_rows(empty))
        conn.execute("CREATE INDEX stems_orth ON stems (orth)")
        conn.execute("CREATE INDEX uniques_orth ON uniques (orth)")
        conn.execute("CREATE INDEX inflects_ending ON inflects (ending)")
        conn.commit()
    finally:
        conn.close()


def connect_mysql(url: str) -> Any:
    """
    Open a PyMySQL connection from a mysql://user:password@host:port/dbname URL.
    PyMySQL is an optional dependency (pip install whitakers_words[mysql]).
    """
    import pymysql

    parts = urlsplit(url)
    return pymysql.connect(
        host=parts.hostname or "127.0.0.1",
        port=parts.port or 3306,
        user=unquote(parts.username or ""),
        password=unquote(parts.password or ""),
        database=parts.path.lstrip("/"),
        charset="utf8mb4",
    )


def _batched(rows: Iterable[Tuple[Any, ...]], size: int = 5000) -> Iterator[list]:
    batch: list = []
    for row in rows:
        batch.append(row)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


# The explicit AUTO_INCREMENT id column replaces sqlite's implicit rowid: the runtime
# layer orders result rows by it to reproduce the generated modules' insertion order.
_MYSQL_SCHEMA = [
    "CREATE TABLE ww_wordlist (id INT PRIMARY KEY, data TEXT NOT NULL)",
    "CREATE TABLE ww_wordkeys (orth VARCHAR(25) PRIMARY KEY)",
    "CREATE TABLE ww_stems (id INT AUTO_INCREMENT PRIMARY KEY, orth VARCHAR(25) NOT NULL,"
    " freq CHAR(1) NOT NULL, data TEXT NOT NULL, KEY ww_stems_orth (orth))",
    "CREATE TABLE ww_uniques (id INT AUTO_INCREMENT PRIMARY KEY, orth VARCHAR(25) NOT NULL,"
    " data TEXT NOT NULL, KEY ww_uniques_orth (orth))",
    "CREATE TABLE ww_inflects (id INT AUTO_INCREMENT PRIMARY KEY, length TINYINT NOT NULL,"
    " ending VARCHAR(8) NOT NULL, age CHAR(1) NOT NULL, freq CHAR(1) NOT NULL,"
    " data TEXT NOT NULL, KEY ww_inflects_ending (ending))",
    "CREATE TABLE ww_empty (pos VARCHAR(8) PRIMARY KEY, data MEDIUMTEXT NOT NULL)",
]

_MYSQL_INSERTS = {
    "ww_wordlist": "INSERT INTO ww_wordlist (id, data) VALUES (%s, %s)",
    "ww_wordkeys": "INSERT INTO ww_wordkeys (orth) VALUES (%s)",
    "ww_stems": "INSERT INTO ww_stems (orth, freq, data) VALUES (%s, %s, %s)",
    "ww_uniques": "INSERT INTO ww_uniques (orth, data) VALUES (%s, %s)",
    "ww_inflects": "INSERT INTO ww_inflects (length, ending, age, freq, data) VALUES (%s, %s, %s, %s, %s)",
    "ww_empty": "INSERT INTO ww_empty (pos, data) VALUES (%s, %s)",
}


def dump_mysql_database(
    url: str,
    wordkeys: Sequence[str],
    wordlist: Sequence[DictEntry],
    stems: Mapping[str, Sequence[Stem]],
    uniques: Mapping[str, Sequence[Unique]],
    inflects: Mapping[Any, Mapping[str, Sequence[Inflect]]],
    empty: Mapping[str, Sequence[Inflect]],
) -> None:
    """
    Write the parsed data to ww_* tables in a MySQL/MariaDB database, so the
    dictionary can share a schema with a consuming application
    """
    data = {
        "ww_wordlist": _wordlist_rows(wordlist),
        "ww_wordkeys": _wordkeys_rows(wordkeys),
        "ww_stems": _stems_rows(stems),
        "ww_uniques": _uniques_rows(uniques),
        "ww_inflects": _inflects_rows(inflects),
        "ww_empty": _empty_rows(empty),
    }
    conn = connect_mysql(url)
    try:
        with conn.cursor() as cursor:
            for table in _MYSQL_INSERTS:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            for statement in _MYSQL_SCHEMA:
                cursor.execute(statement + " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
            for table, insert in _MYSQL_INSERTS.items():
                for batch in _batched(data[table]):
                    cursor.executemany(insert, batch)
        conn.commit()
    finally:
        conn.close()


def generate_database(path: Optional[str] = None) -> None:
    """
    Build the sqlite database from the generated python modules, for installations
    that already have those but no database file yet
    """
    from .generated.empty import empty
    from .generated.inflects import inflects
    from .generated.stems import stems
    from .generated.uniques import uniques
    from .generated.wordkeys import wordkeys
    from .generated.wordlist import wordlist

    if path is None:
        from .datalayer import default_database_path

        path = default_database_path()
    dump_database(path, wordkeys, wordlist, stems, uniques, inflects, empty)


def generate_mysql_database(url: str) -> None:
    """
    Build the ww_* MySQL tables from the generated python modules, for installations
    that already have those (see generate_database for the sqlite equivalent)
    """
    from .generated.empty import empty
    from .generated.inflects import inflects
    from .generated.stems import stems
    from .generated.uniques import uniques
    from .generated.wordkeys import wordkeys
    from .generated.wordlist import wordlist

    dump_mysql_database(url, wordkeys, wordlist, stems, uniques, inflects, empty)


def generate_all_dicts(path: Optional[str] = None) -> None:
    gen = Generator()
    gen.create_init_file()
    wordkeys, wordlist, stems = gen.import_dicts()
    gen.import_affixes()
    uniques = gen.import_uniques()
    empty, inflects = gen.import_inflects()
    if path is None:
        from .datalayer import default_database_path

        path = default_database_path()
    dump_database(path, wordkeys, wordlist, stems, uniques, inflects, empty)
