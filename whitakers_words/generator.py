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
            if len(line) > 0 and not line.startswith("--"):
                n = []

                # Nouns

                # No ending
                if i in range(26, 41):

                    n = parse_infl_type(line[7:21])

                    data.append({
                        'ending': "",
                        'n': n,
                        'note': "",
                        'pos': line[0:7].strip(),
                        'form': line[7:21].strip()
                    })

                # 1st declension
                elif i in range(63, 86):

                    n = parse_infl_type(line[6:9])

                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # 1st declension Greek
                elif i in range(93, 100):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(103, 114):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(118, 128):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Second declension
                elif i in range(137, 160):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(166, 176):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Second declension er
                elif i in range(183, 187):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "er",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Second declension ius / ium
                elif i in range(194, 202):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "ius/ium",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Second declension ius / ium
                elif i in range(209, 215):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "ius/ium",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Second declension greek
                elif i in range(220, 230):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(236, 246):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(250, 255):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(261, 266):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Third declension
                elif i in range(279, 302):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(307, 316):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "stem_ends_in_cons",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(324, 337):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "i-stems_m-f",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(343, 352):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "i-stems_n",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Third declension greek
                elif i in range(357, 364):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(367, 378):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(384, 398):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(407, 436):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Fourth declension
                elif i in range(442, 466):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Fourth declension u
                elif i in range(470, 480):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "u",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(484, 491):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "jesus_jesu",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Fifth declension
                elif i in range(495, 514):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Abbreviations
                elif i in range(517, 519):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': '',
                        'n': n,
                        'note': "abbreviation",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Not declined
                elif i in range(520, 522):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': '',
                        'n': n,
                        'note': "not_declined",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Adjective

                # First declension
                elif i in range(531, 569):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:34].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(574, 604):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:34].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(610, 652):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:34].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(659, 673):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:34].strip(),
                        'n': n,
                        'note': "first_and_second",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(676, 735):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:34].strip(),
                        'n': n,
                        'note': "nullus_alius",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(742, 750) or i in range(759, 795):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[23:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Third declension adj
                elif i in range(751, 758) or i in range(796, 813):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(820, 853):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:33].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(858, 870):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:33].strip(),
                        'n': n,
                        'note': "two_endings",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(874, 886):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:33].strip(),
                        'n': n,
                        'note': "three_endings",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })
                elif i in range(891, 906):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[28:33].strip(),
                        'n': n,
                        'note': "greek",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Verbs

                # First conjugation
                elif i in range(916, 1085):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # Second conjugation
                elif i in range(1101, 1224):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # Third conjugation
                elif i in range(1237, 1366):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })
                elif i in range(1375, 1514):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "irregular",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # Fourth conjugation
                elif i in range(1524, 1623):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # Esse
                elif i in range(1633, 1742):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "like_to_be",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # ire
                elif i in range(1754, 1921):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:50].strip(),
                        'n': n,
                        'note': "eo_ire",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # velle, malle, nolle`
                elif i in range(1933, 2000):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "velle",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # defective
                elif i in range(2015, 2147):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "defective",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # kludge
                elif i in range(2161, 2127):

                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[38:52].strip(),
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:34].strip()
                    })

                # abbreviations
                elif i in range(2196, 2201):
                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': "",
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:28].strip()
                    })

                # Participles / Supine

                # participles 1-3
                elif i in range(2208, 2682):

                    n = parse_infl_type(line[5:8])
                    data.append({
                        'ending': line[38:51].strip(),
                        'n': n,
                        'note': "participles",
                        'pos': line[0:5].strip(),
                        'form': line[9:34].strip()
                    })

                # supine
                elif i in range(2691, 2694):
                    n = parse_infl_type(line[7:10])
                    data.append({
                        'ending': line[24:30].strip(),
                        'n': n,
                        'note': "supine",
                        'pos': line[0:7].strip(),
                        'form': line[11:20].strip()
                    })

                # Pronouns
                elif i in range(2697, 2700):
                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': "",
                        'n': n,
                        'note': "",
                        'pos': line[0:6].strip(),
                        'form': line[10:28].strip()
                    })

                elif i in range(2756, 3028):
                    n = parse_infl_type(line[6:9])
                    data.append({
                        'ending': line[24:52].strip(),
                        'n': n,
                        'note': "pronoun",
                        'pos': line[0:6].strip(),
                        'form': line[10:17].strip()
                    })

                # Numerals
                elif i in range(3035, 3193):
                    n = parse_infl_type(line[7:10])
                    data.append({
                        'ending': line[32:42].strip(),
                        'n': n,
                        'note': "numeral",
                        'pos': line[0:7].strip(),
                        'form': line[11:19].strip()
                    })
                elif i in range(3196, 3205):
                    n = parse_infl_type(line[7:10])
                    data.append({
                        'ending': line[36:42].strip(),
                        'n': n,
                        'note': "numeral",
                        'pos': line[0:7].strip(),
                        'form': line[11:19].strip()
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
