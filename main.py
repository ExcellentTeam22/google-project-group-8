from dataclasses import dataclass
from typing import List
from string import ascii_lowercase
from pathlib import Path
import string

# from autocomplete import AutoCompleter

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
    pass
    # temp = []
    # for file in MY_LIST:
    #     for sentence in file.sentences:
    #         if prefix.lower() in sentence.lower():
    #             temp.append(AutoCompleteData(sentence, file.file_name, len(prefix), len(prefix) * 2))
    # return temp


@dataclass
class TextData:
    file_name: str
    sentences: List[str]


def get_matches(current_sentence, matches):
    for sentences in MY_LIST:
        for sentence in sentences.sentences:
            if current_sentence in sentence:
                matches.append(AutoCompleteData(sentence, sentences.file_name, 20, 20))


def compare(the_input: str):
    matches = []
    get_matches(my_input, matches)

    for i in range(len(the_input)):
        print(i)
        remove_cell = the_input[:i] + the_input[i + 1:]
        get_matches(remove_cell, matches)

        for c in ascii_lowercase:
            add_cell = the_input[:i] + c + the_input[i+1:]
            print(add_cell)
            get_matches(add_cell, matches)
        for c in ascii_lowercase:
            if c != the_input[i]:
                change_cell = the_input[:i] + c + the_input[i + 1:]
                get_matches(change_cell, matches)
    return matches


if __name__ == '__main__':

    with open(r'text.txt', encoding='utf-8') as f:
        MY_LIST.append(TextData(str(f), [line for line in f]))

    my_input = input("Enter Search:")
    result = get_best_k_completions(my_input)

    if result:
        print(result)
    else:
        compare(my_input)
