from dataclasses import dataclass
from typing import List


MATCHES = set()

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int
# methods that you need to define by yourself


def build_database():
    pass


def initialization(path):
    f = open(path, 'r', encoding='utf-8')
    all_lines = f.readlines()
    f.close()
    return all_lines


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    pass


if __name__ == '__main__':
    from pathlib import Path
    files = list(Path("Archive").rglob("*.[tT][xX][tT]"))
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            MATCHES.update({line for line in f})

    print(get_best_k_completions(input("Enter Search")))