"""
datagenerator.py

Format the data from the input files from Whitaker's Words into python dictionaries
and an equivalent sqlite database
"""
import json
import os
import sqlite3
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

from .datatypes import DictEntry, Inflect, Stem, Unique


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
                parts = [x.lower() for x in parts]
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
                    obj["orth"] = line.strip()

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

        conn.executemany(
            "INSERT INTO wordlist VALUES (?, ?)",
            ((i, json.dumps(entry)) for i, entry in enumerate(wordlist)),
        )
        conn.executemany(
            "INSERT INTO wordkeys VALUES (?)", ((key,) for key in set(wordkeys))
        )
        conn.executemany(
            "INSERT INTO stems VALUES (?, ?, ?)",
            (
                (orth, stem["props"][3], json.dumps(stem))
                for orth, stem_list in stems.items()
                for stem in stem_list
            ),
        )
        conn.executemany(
            "INSERT INTO uniques VALUES (?, ?)",
            (
                (orth, json.dumps(unique))
                for orth, unique_list in uniques.items()
                for unique in unique_list
            ),
        )
        conn.executemany(
            "INSERT INTO inflects VALUES (?, ?, ?, ?, ?)",
            (
                (int(length), ending, infl["props"][0], infl["props"][1], json.dumps(infl))
                for length, ending_list in inflects.items()
                for ending, infl_list in ending_list.items()
                for infl in infl_list
            ),
        )
        conn.executemany(
            "INSERT INTO empty VALUES (?, ?)",
            ((pos, json.dumps(infl_list)) for pos, infl_list in empty.items()),
        )
        conn.execute("CREATE INDEX stems_orth ON stems (orth)")
        conn.execute("CREATE INDEX uniques_orth ON uniques (orth)")
        conn.execute("CREATE INDEX inflects_ending ON inflects (ending)")
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
