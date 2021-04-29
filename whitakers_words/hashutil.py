import hashlib
import os


def hash_file(filepath: str) -> str:
    file_hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            buffer = f.read(65536)
            if not buffer:
                break
            file_hash.update(buffer)
    return file_hash.hexdigest()


def hash_generated_files() -> dict[str, str]:
    folder = 'whitakers_words/generated/'
    result: dict[str, str] = dict()
    for f in os.listdir(folder):
        if not f.startswith("__"):
            value = hash_file(folder + f)
            result[f] = value
    return result


if __name__ == "__main__":
    for x in hash_generated_files().items():
        print(x)
