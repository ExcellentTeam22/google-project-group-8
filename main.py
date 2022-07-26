from dataclasses import dataclass
from typing import List
from string import ascii_lowercase
from pathlib import Path
# from autocomplete import AutoCompleter
import os

MAX_QUERIES = 5

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


class TrieNode:
    def __init__(self, word):
        self.word = word
        self.is_end = False
        self.counter = 0
        self.children = {}
        self.filename = ""


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, line, filename):
        node = self.root
        for word in line.split():
            if word in node.children:
                node = node.children[word]
            else:
                new_node = TrieNode(word)
                node.children[word] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1
        node.filename = filename

    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix, node.counter, node.filename))
        for child in node.children.values():
            self.dfs(child, prefix + " " + child.word)

    def search(self, prefix, last_word_prefix):
        completed_words = True
        self.output = []
        node = self.root
        for word in prefix.split():
            if word in node.children:
                node = node.children[word]
            else:
                found_word_contains_last_word_pref = False
                for n in node.children:
                    if str(n).startswith(last_word_prefix):
                        found_word_contains_last_word_pref = True
                        completed_words = False
                if not found_word_contains_last_word_pref:
                    return []

        prefix = prefix if completed_words else prefix.rsplit(' ', 1)[0]
        self.dfs(node, prefix)
        # if len(self.output) < MAX_QUERIES:
        return sorted(self.output, key=lambda x: x[1], reverse=True)


def insert_to_tree(t: Trie, dictionary: dict):
    files = list(Path("Archive").rglob("*.[tT][xX][tT]"))
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            filename = os.path.basename(f.name)
            for line in f.readlines():
                t.insert(line, filename)
                # dictionary[line] = filename


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    lst = []
    pass


if __name__ == '__main__':
    tree = Trie()
    dictionary_filename_sentences = {}
    insert_to_tree(tree, dictionary_filename_sentences)
    inp = ""

    while True:
        current = input(f"Enter search: {inp}")
        if current == '#':
            inp = input("Enter new search pattern: ")
        else:
            inp += current
        print(tree.search(inp, inp.rsplit(None, 1)[-1]))





# def get_score(e):
#     return e.score
#
#
# def initialization(path):
#     f = open(path, 'r', encoding='utf-8')
#     all_lines = f.readlines()
#     f.close()
#     return all_lines