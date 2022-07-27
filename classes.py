import string
from dataclasses import dataclass

MAX_QUERIES = 5


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


class TrieNode:
    def __init__(self, word: str):
        self.word = str(word).lower()
        self.is_end = False
        self.counter = 0
        self.children = {}
        self.filename = ""


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    def insert(self, line: str, filename: str):
        node = self.root
        for word in line.split():
            word = str(word).lower()
            if word in node.children:
                node = node.children[word]
            else:
                new_node = TrieNode(word)
                node.children[word] = new_node
                node = new_node
        node.is_end = True
        node.counter += 1
        node.filename = filename

    @staticmethod
    def dfs(node: TrieNode, prefix: str, output, length):
        if node.is_end:
            output.append((prefix, node.counter, node.filename))
        for child in node.children.values():
            if len(output) < length:
                Trie.dfs(child, f"{prefix} {child.word}", output, MAX_QUERIES)
            else:
                break

    def search(self, prefix: str, last_word_prefix: str):
        output = []
        sentence_match = True
        node = self.root
        for word in prefix.split():
            word = str(word).lower()
            last_node = node
            if word in node.children:
                node = node.children[word]
            else:
                sentence_match = False
        if sentence_match:
            self.dfs(node, prefix, output, MAX_QUERIES)

        node = last_node
        if len(output) <= MAX_QUERIES:
            for key in node.children.keys():
                if key.startswith(last_word_prefix):
                    self.dfs(node.children[key], f"{prefix.rsplit(' ', 1)[0]} {key}", output, MAX_QUERIES)
        if len(output) <= MAX_QUERIES:
            # temp = ""
            # for index in len(prefix):
            #     temp = prefix[:index] + prefix[index + 1:]

                # check for match and add to ouput
            node = self.root
            for word in prefix.split():
                word = str(word).lower()
                if word in node.children:
                    node = node.children[word]
                else:
                    for child in node.children.keys():
                        if len(child) == len(word) - 1:
                            for index in range(len(word)):
                                if child == word[:index] + word[index + 1:]:
                                    node = node.children[child]
                                    prefix = prefix.replace(word,child)
                                    break

            self.dfs(node, prefix, output, MAX_QUERIES)
        return sorted(output, key=lambda x: x[1], reverse=True)
