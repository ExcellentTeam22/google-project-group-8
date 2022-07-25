from dataclasses import dataclass
from typing import List


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    pass


if __name__ == '__main__':
    from pathlib import Path

    files = list(Path("Archive").rglob("*.[tT][xX][tT]"))
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            pass
