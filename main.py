from dataclasses import dataclass
from typing import List
from pathlib import Path
import string
from autocomplete import AutoCompleter

MY_LIST = []


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


# methods that you need to define by yourself


def build_database():
    pass


def get_score(e):
    return e.score

def initialization(path):
    f = open(path, 'r', encoding='utf-8')
    all_lines = f.readlines()
    f.close()
    return all_lines


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    temp = []
    for file in MY_LIST:
        for sentence in file.sentences:
            if prefix.lower() in sentence.lower():
                temp.append(AutoCompleteData(sentence, file.file_name, len(prefix), len(prefix) * 2))
    return temp


@dataclass
class TextData:
    file_name: str
    sentences: List[str]


def compare(the_input: str):

    for ch in the_input:
        for letter in string.ascii_lowercase[:26]:

            print(letter)


if __name__ == '__main__':

    with open(r'text.txt', encoding='utf-8') as f:
        MY_LIST.append(TextData(str(f), [line for line in f]))

    my_input = input("Enter Search:")
    result = get_best_k_completions(my_input)

    if result:
        print(result)
    else:
        compare(my_input)

