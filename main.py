from dataclasses import dataclass
from typing import List

from autocomplete import AutoCompleter

import sqlite3       

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


if __name__=='__main__':

    pass
