from collections import Counter
from datetime import datetime, timezone
from pathlib import Path as Pathh
from random import randrange


def are_all_the_same(a_list: list) -> bool:
    return 1 == len(Counter(a_list).values())


def slurp(pathname: str) -> str:
    return Pathh(pathname).read_text()


def string_to_lines(string_containing_newlines: str) -> list[str]:
    return string_containing_newlines.splitlines()


def file_as_list_of_lines(pathname: str) -> list[str]:
    return string_to_lines(slurp(pathname))


def head_on_str(a_string: str, lines_count: int = 5) -> str:
    return "\n".join(string_to_lines(a_string)[:lines_count])


def head(path: str, lines_count: int = 5) -> str:
    result = f"{path} do not exists"
    if file_exists(path):
        result = head_on_str(slurp(path), lines_count)
    return result


def line_count(s: str) -> int:
    return len(string_to_lines(s))


def file_exists(path_to_file: str) -> bool:
    return Pathh(path_to_file).is_file()


def now():
    return datetime.now(timezone.utc)


def one_line(s):
    return str(s).replace("\n", "")


def ln(s):
    return one_line(s)


def ls(s, lenght=65):
    return f"{ln(s)[0:lenght]}..."


def loggable_bytes(b: bytes):
    return b.replace(b"\n", b" ")


def save_file_on_local_storage(content: str, pathname: str):
    with open(pathname, "w") as f:
        f.write(content)
    return pathname


def remove_duplicates(a_list: list) -> list:
    return list(set(a_list))


def sorted_uniqued(a_list: list) -> list:
    result = remove_duplicates(a_list)
    result.sort()
    return result


def non_unique_elements(a_list: list) -> list:
    result = []
    counter = Counter(a_list)
    for k, v in counter.items():
        if v > 1:
            result.append(k)
    return result


def file_as_bytes(file):
    with file:
        return file.read()


def contains(a_string, b_string) -> bool:
    return b_string in a_string


def contains_any(a_string, strings: list[str]) -> bool:
    result = False
    for s in strings:
        if s in a_string:
            result = True
            break
    return result


def random_in_range(start, stop):
    return randrange(start, stop)


def line(number: int, multiline_string: str) -> str:
    return multiline_string.split("\n")[number]


def list_of_elements(dictionary: dict) -> list[dict]:
    return [{k: v} for k, v in dictionary.items()]


if __name__ == '__main__':
    a = [0, 1]
    b = [0, 0]
    print(f"a are {'' if are_all_the_same(a) else 'NOT '}all the same")
    print(f"a are {'' if are_all_the_same(b) else 'NOT '}all the same")
