import hashlib
import os


def hash_file(filepath: str) -> str:
    file_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        while buffer := f.read(65536):
            file_hash.update(buffer)
    return file_hash.hexdigest()


def hash_generated_files() -> dict[str, str]:
    folder = "whitakers_words/generated/"
    result: dict[str, str] = dict()
    for f in os.listdir(folder):
        if not f.startswith("__"):
            value = hash_file(folder + f)
            result[f] = value
    return result


def make_ordinal(n: int) -> str:
    '''
    LICENSE NOTICE
    I found this function on https://stackoverflow.com/a/50992575/2065017.
    As a result, it is licensed under the CC BY-SA 4.0 license.
    I have added type hints in the function definition.

    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
