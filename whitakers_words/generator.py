"""
generator.py

Format the data from the input files from Whitaker's Words into python dictionaries

"""

import json
import os
from pkg_resources import resource_filename


resources_directory = resource_filename(__name__, "data")
files_directory = resources_directory[:-4] + "generated/"
try:
    os.mkdir(files_directory)
except FileExistsError:
    pass

def dump_file(name, obj=None):
    with open(files_directory + name, 'w') as out:
        if obj:
            out.write(name[:-3] + " = ")
            json.dump(obj, out)
        out.write("\n")


def import_dicts():
    keys = list()
    ids = ['']
    stems = dict()
    previous_item = None
    with open(resources_directory + '/DICTLINE.GEN', encoding="ISO-8859-1") as f:
        for i, line in enumerate(f):

            orth = line[0:19].replace("zzz", "-").strip()
            parts = [orth]

            if len(line[19:38].strip()) > 0:
                parts.append(line[19:38].replace("zzz", "-").strip())

            if len(line[38:57].strip()) > 0:
                parts.append(line[38:57].replace("zzz", "-").strip())

            if len(line[57:76].strip()) > 0:
                parts.append(line[57:76].replace("zzz", "-").strip())

            if len(line[83:87].strip()) > 0:
                n = line[83:87].strip().split(" ")
                for n_i, v in enumerate(n):
                    try:
                        n[n_i] = int(v)
                    except ValueError:
                        pass

            senses = line[109:].strip().split(";")
            new_senses = []
            for sense in senses:
                sense = sense.strip()
                if len(sense):
                    new_senses.append(sense)
            else:
                item = {
                    'id': i + 1,
                    'orth': orth,
                    'parts': parts,
                    'pos': line[76:83].strip(),
                    'form': line[83:100].strip(),
                    'n': n,
                    'senses': new_senses
                }
                for part in parts:
                    stem = {
                        'orth': part,
                        'pos': line[76:83].strip(),
                        'form': line[83:100].strip(),
                        'n': n,
                        'wid': i + 1
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
    dump_file('dict_keys.py', keys)
    dump_file('dict_ids.py', ids)
    dump_file('stems.py', stems)


def import_suffixes():
    with open(resources_directory + '/suffixes.txt') as f:

        i = 0
        obj = {}
        data = []

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


def import_prefixes():
    with open(resources_directory + '/prefixes.txt') as f:

        i = 0
        obj = {}
        data = []

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


def import_uniques():
    with open(resources_directory + '/UNIQUES.LAT') as f:

        i = 0
        obj = {}
        data = dict()
        x = str()
        for line in f:

            if i == 0:
                obj['orth'] = line.strip()

            elif i == 1:
                space = line.find(" ")
                obj['pos'] = line[:space].strip()
                obj['form'] = line[space:52].strip()

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

    dump_file('uniques.py', data)


def import_inflects():
    with open(resources_directory + '/INFLECTS.LAT') as f:

        i = 0
        obj = {}
        data = []
        for i, text in enumerate(f):
            line = text.strip()
            if not len(line) > 0 or line.startswith('--'):
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
            if pos == 'ADV':
                n = info[-4:-2]
                form = [info[1]]
            elif pos in ('PREP', 'CONJ', 'INTERJ'):
                n = info[-4:-2]
                form = info[1:-2]

            elif pos == 'V':
                form = info[3:8]

            elif pos == 'ADJ':
                form = info[3:7]

            elif pos in ('N', 'VPAR', 'SUPINE', 'PRON', 'NUM'):
                form = info[3:6]

            else:
                raise Exception()
            data.append({
                'ending': ending,
                'n': [int(i) for i in n],
                'note': comment,
                'pos': pos,
                'form': ' '.join(form)
            })

    reordered = reorder_inflects(data)
    dump_file('inflects.py', reordered)


def reorder_inflects(data):
    keys = (x for x in range(8))  # assuming all endings are between 0 and 7 in length
    result = {key: dict() for key in keys}
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


def parse_infl_type(s):
    if len(s.strip()) > 0:
        n = s.strip().split(" ")
        for i, v in enumerate(n):
            try:
                n[i] = int(v)
            except ValueError:
                pass

    return n


def create_init_file():
    dump_file("__init__.py")


def generate_all_dicts():
    create_init_file()
    import_dicts()
    import_suffixes()
    import_prefixes()
    import_uniques()
    import_inflects()
