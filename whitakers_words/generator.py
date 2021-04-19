"""
generator.py

Format the data from the input files from Whitaker's Words into python dictionaries

"""

import json
import os
from typing import Any, Sequence, Union

from pkg_resources import resource_filename

from .datatypes import DictEntry, Stem, Unique

stems_imports = "Stem"
stems_definition = "dict[str, Sequence[Stem]]"
inflects_imports = "Inflect"
inflects_definition = "dict[str, dict[str, Sequence[Inflect]]]"
uniques_imports = "Unique"
uniques_definition = "dict[str, Sequence[Unique]]"
dictentry_imports = "DictEntry"
dictentry_definition = "Sequence[DictEntry]"
dictkeys_definition = "list[str]"

resources_directory = resource_filename(__name__, "data")
files_directory = resources_directory[:-4] + "generated/"
try:
    os.mkdir(files_directory)
except FileExistsError:
    pass


def dump_file(name: str, obj: Any = None, definition: str = '', imports: str = '') -> None:
    with open(files_directory + name, 'w') as out:
        if obj:
            if "Sequence" in definition:
                out.write("from typing import Sequence\n")
            if imports:
                out.write(f"from whitakers_words.datatypes import {imports}\n\n")
            local_def = f": {definition}" if definition else ""
            out.write(f"{name[:-3]}{local_def} = ")
            json.dump(obj, out)
        out.write("\n")


def import_dicts() -> None:
    keys: Sequence[str] = list()
    ids: Sequence[DictEntry] = [{}]
    stems: dict[str, Sequence[Stem]] = dict()
    previous_item: DictEntry = {}
    with open(resources_directory + '/DICTLINE.GEN', encoding="ISO-8859-1") as f:
        for i, line in enumerate(f):
            parts = line[:76].replace("zzz", "-").split()

            orth = parts[0]

            pos = line[76:83].strip()

            raw_form = line[83:100].strip()

            properties = line[100:110].split()

            n: Sequence[int] = []
            form: Sequence[Union[str, int]] = []
            for v in raw_form.split():
                try:
                    val = int(v)
                    if val > 9:
                        form.append(val)
                    else:
                        n.append(val)
                except ValueError:
                    form.append(v)

            senses = line[109:].strip().split(";")
            new_senses = []
            for sense in senses:
                sense = sense.strip()
                if sense:
                    new_senses.append(sense)
            item: DictEntry = {
                'id': i + 1,
                'orth': orth,
                'parts': parts,
                'pos': pos,
                'form': form,
                'n': n,
                'senses': new_senses
            }
            for part in parts:
                stem: Stem = {
                    'orth': part,
                    'pos': pos,
                    'form': form,
                    'n': n,
                    'wid': i + 1,
                    'props': properties
                }
                if part in stems:
                    items = stems[part]
                    items.append(stem)
                    stems[part] = items
                else:
                    stems[part] = [stem]
            if senses[0][0] == '|':
                new_senses[0] = new_senses[0].replace("|", "")
                previous_item['senses'].extend(new_senses)
                ids.append(dict())
            else:
                keys.extend(parts)
                ids.append(item)
                previous_item = item

    keys = list(set(keys))
    keys.sort()
    dump_file('wordkeys.py', keys, dictkeys_definition)
    dump_file('wordlist.py', ids, dictentry_definition, dictentry_imports)
    dump_file('stems.py', stems, stems_definition, stems_imports)


def import_suffixes() -> None:
    with open(resources_directory + '/suffixes.txt') as f:

        i = 0
        obj: Unique = {}
        data: Sequence[Unique] = []

        for line in f:

            if i == 0:
                obj['orth'] = line.replace("PREFIX", "").replace("SUFFIX", "").strip()

            elif i == 1:
                obj['pos'] = line[0].strip()
                obj['form'] = line[0:].strip()

            elif i == 2:
                obj['senses'] = [line.strip()]

            i = i + 1
            if i == 3:
                data.append(obj)
                obj = {}
                i = 0

    dump_file('suffixes.py', data)


def import_prefixes() -> None:
    with open(resources_directory + '/prefixes.txt') as f:

        i = 0
        obj: Unique = {}
        data: Sequence[Unique] = []

        for line in f:

            if i == 0:
                obj['orth'] = line.replace("PREFIX", "").strip()

            elif i == 1:
                obj['pos'] = line[0].strip()
                obj['form'] = line[0:].strip()

            elif i == 2:
                obj['senses'] = [line.strip()]

            i = i + 1
            if i == 3:
                data.append(obj)
                obj = {}
                i = 0

    dump_file('prefixes.py', data)


def import_uniques() -> None:
    with open(resources_directory + '/UNIQUES.LAT') as f:

        i = 0
        obj: Unique = {}
        data: dict[str, Sequence[Unique]] = dict()
        for line in f:

            if i == 0:
                obj['orth'] = line.strip()

            elif i == 1:
                ite = line.split()
                obj['pos'] = ite[0]
                obj['n'] = [int(x) for x in ite[1:3]]
                obj['form'] = ite[3:-5]

            elif i == 2:
                obj['senses'] = [line.strip()]

            i = i + 1
            if i == 3:
                orth = obj['orth']
                if orth in data:
                    items = data[orth]
                    items.append(obj)
                    data[orth] = items
                else:
                    data[orth] = [obj]
                obj = {}
                i = 0

    from whitakers_words.data.esse import esse
    for est in esse:
        orth = est['orth']
        if orth in data:
            items = data[orth]
            items.append(est)
            data[orth] = items
        else:
            data[orth] = [est]

    dump_file('uniques.py', data, uniques_definition, uniques_imports)


# TODO use info[-5], it determines which stem the inflection latches onto
def import_inflects() -> None:
    with open(resources_directory + '/INFLECTS.LAT') as f:

        i = 0
        data = []
        for i, text in enumerate(f):
            line = text.strip()
            if not line or line.startswith('--'):
                continue
            comment = ''

            if '--' in line:
                comment = line[line.index('--') + 2:].strip()
                line = line[:line.index('--')]
            info = line.split()

            ending = info[-3]
            if not ending.isalpha():
                ending = ''
            pos = info[0]
            n = info[1:3]
            properties = info[-2:]
            if pos == 'ADV':
                n = info[-4:-2]
                form = [info[1]]
            elif pos in ('PREP', 'CONJ', 'INTERJ'):
                n = info[-4:-2]
                form = info[1:-2]

            elif pos in ('V', 'VPAR'):
                form = info[3:8]

            elif pos == 'ADJ':
                form = info[3:7]

            elif pos in ('N', 'SUPINE', 'PRON', 'NUM'):
                form = info[3:6]

            else:
                raise Exception()
            data.append({
                'ending': ending,
                'n': [int(x) for x in n],
                'note': comment,
                'pos': pos,
                'form': form,
                'props': properties,
                'iid': i
            })

    reordered = reorder_inflects(data)
    dump_file('inflects.py', reordered, inflects_definition, inflects_imports)


def reorder_inflects(data: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    keys = (x for x in range(8))  # assuming all endings are between 0 and 7 in length
    result: dict[int, dict[str, Any]] = {key: dict() for key in keys}
    for item in data:
        end = item['ending']
        store = result[len(end)]
        if end in store:
            items = store[end]
            items.append(item)
            store[end] = items
        else:
            store[end] = [item]
    return result


def create_init_file() -> None:
    dump_file("__init__.py")


def generate_all_dicts() -> None:
    create_init_file()
    import_dicts()
    import_suffixes()
    import_prefixes()
    import_uniques()
    import_inflects()
