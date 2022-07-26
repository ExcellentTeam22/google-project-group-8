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
    def dfs(node: TrieNode, prefix: str, output):
        if node.is_end:
            output.append((prefix, node.counter, node.filename))
        for child in node.children.values():
            Trie.dfs(child, f"{prefix} {child.word}", output)

    def search(self, prefix: str, last_word_prefix: str):
        completed_words = True
        output = []
        list_of_children = []
        node = self.root
        for word in prefix.split():
            word = str(word).lower()
            if word in node.children:
                node = node.children[word]
            else:
                found_word_contains_last_word_pref = False
                for child_word, child_node in node.children.items():
                    if str(child_word).startswith(last_word_prefix):
                        found_word_contains_last_word_pref = True
                        completed_words = False
                        list_of_children.append(child_node)
                if not found_word_contains_last_word_pref:
                        for child in node.children:
                            if len(set(child) & set(word)) == len(child):# we need to delete a letter
                                for letter in word:
                                    if word.replace(letter, "") == child:
                                        prefix=prefix.replace((word,child))

                            else:
                                if len(child) == len(word):  # we need to change a letter
                                    for letter in word:
                                        for letter_in_alphabet in string.ascii_lowercase:
                                            if word.replace(letter, letter_in_alphabet) == child:
                                                prefix = prefix.replace(word, child)
                                else:
                                    break
                            return []  # here we need to delete/insert/replace a character

        prefix = prefix if completed_words else prefix.rsplit(' ', 1)[0]
        if not completed_words:
            for n in list_of_children:
                self.dfs(n, f"{prefix} {n.word}", output)
        else:
            self.dfs(node, prefix, output)
        # if len(self.output) < MAX_QUERIES:
        return sorted(output, key=lambda x: x[1], reverse=True)