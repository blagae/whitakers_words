"""
generator.py

Format the data from the input files from Whitaker's Words into python dictionaries
"""
import json
import os
from typing import Any, Sequence, Union

from pkg_resources import resource_filename

from .datatypes import DictEntry, Stem, Unique


class Generator:
    def __init__(self) -> None:
        self.resources = resource_filename(__name__, "data")
        self.filedir = self.resources[:-4] + "generated/"
        try:
            os.mkdir(self.filedir)
        except FileExistsError:
            pass

    def dump_file(self, name: str, obj: Any = None, definition: str = '', imports: str = '') -> None:
        with open(self.filedir + name, 'w') as out:
            if obj:
                if "Sequence" in definition:
                    out.write("from typing import Sequence\n\n")
                if imports:
                    out.write(f"from whitakers_words.datatypes import {imports}\n\n")
                local_def = f": {definition}" if definition else ""
                out.write(f"{name[:-3]}{local_def} = ")
                json.dump(obj, out)
            out.write("\n")

    def import_dicts(self) -> None:
        keys: Sequence[str] = list()
        ids: Sequence[DictEntry] = [{}]
        stems: dict[str, Sequence[Stem]] = dict()
        previous_item: DictEntry = {}
        with open(self.resources + '/DICTLINE.GEN', encoding="ISO-8859-1") as f:
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

                senses = [sense.strip() for sense in line[109:].strip().split(";") if sense]

                item: DictEntry = {
                    'id': i + 1,
                    'orth': orth,
                    'parts': parts,
                    'pos': pos,
                    'form': form,
                    'n': n,
                    'senses': senses
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
                    senses[0] = senses[0].replace("|", "")
                    previous_item['senses'].extend(senses)
                    ids.append(dict())
                else:
                    keys.extend(parts)
                    ids.append(item)
                    previous_item = item

        self.dump_file('wordkeys.py', keys, "list[str]")
        self.dump_file('wordlist.py', ids, "Sequence[DictEntry]", "DictEntry")
        self.dump_file('stems.py', stems, "dict[str, Sequence[Stem]]", "Stem")

    def import_affixes(self) -> None:
        for affix in ["prefix", "suffix"]:
            with open(f"{self.resources}/{affix}es.txt") as f:

                counter = 0
                obj: Unique = {}
                data: Sequence[Unique] = []

                for line in f:
                    if counter == 0:
                        obj['orth'] = line.replace(affix.upper(), "").strip()

                    elif counter == 1:
                        obj['pos'] = line[0].strip()
                        obj['form'] = line[0:].strip()

                    elif counter == 2:
                        obj['senses'] = line.strip().split()

                    counter += 1
                    if counter == 3:
                        data.append(obj)
                        obj = {}
                        counter = 0

            self.dump_file(f'{affix}es.py', data)

    def import_uniques(self) -> None:
        with open(self.resources + '/UNIQUES.LAT') as f:

            counter = 0
            obj: Unique = {}
            data: dict[str, Sequence[Unique]] = dict()
            for line in f:
                if counter == 0:
                    obj['orth'] = line.strip()

                elif counter == 1:
                    contents = line.split()
                    obj['pos'] = contents[0]
                    obj['n'] = [int(x) for x in contents[1:3]]
                    obj['form'] = contents[3:-5]

                elif counter == 2:
                    obj['senses'] = line.strip().split()

                counter += 1
                if counter == 3:
                    orth = obj['orth']
                    if orth in data:
                        items = data[orth]
                        items.append(obj)
                        data[orth] = items
                    else:
                        data[orth] = [obj]
                    obj = {}
                    counter = 0

        from whitakers_words.data.esse import esse
        for est in esse:
            orth = est['orth']
            if orth in data:
                items = data[orth]
                items.append(est)
                data[orth] = items
            else:
                data[orth] = [est]

        self.dump_file('uniques.py', data, "dict[str, Sequence[Unique]]", "Unique")

    def import_inflects(self) -> None:
        # TODO use info[-5], it determines which stem the inflection latches onto
        with open(self.resources + '/INFLECTS.LAT') as f:
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

        reordered = self.reorder_inflects(data)
        self.dump_file('inflects.py', reordered, "dict[str, dict[str, Sequence[Inflect]]]", "Inflect")

    def reorder_inflects(self, data: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
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

    def create_init_file(self) -> None:
        self.dump_file("__init__.py")


def generate_all_dicts() -> None:
    gen = Generator()
    gen.create_init_file()
    gen.import_dicts()
    gen.import_affixes()
    gen.import_uniques()
    gen.import_inflects()
