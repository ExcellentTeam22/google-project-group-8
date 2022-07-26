from dataclasses import dataclass
from typing import List
from string import ascii_lowercase
from pathlib import Path
# from autocomplete import AutoCompleter


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1

    def dfs(self, node, prefix):
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def search(self, prefix):
        self.output = []
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        self.dfs(node, prefix[:-1])
        return sorted(self.output, key=lambda x: x[1], reverse=True)


def insert_to_tree(t: Trie):
    files = list(Path("Archive").rglob("*.[tT][xX][tT]"))
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                for word in line.split():
                    if word.isalpha():
                        t.insert(word.lower())


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    lst = []
    pass


if __name__ == '__main__':
    tree = Trie()

    insert_to_tree(tree)

    inp = input("Enter search: ")
    while inp != '#':
        print(tree.search(inp))
        inp = input("Enter search: ")





# def get_score(e):
#     return e.score
#
#
# def initialization(path):
#     f = open(path, 'r', encoding='utf-8')
#     all_lines = f.readlines()
#     f.close()
#     return all_lines