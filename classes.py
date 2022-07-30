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
        node.filename = filename

    @staticmethod
    def dfs(node: TrieNode, prefix: str, score, output, length):
        if node.is_end and not (prefix, score, node.filename) in output:
            output.append((prefix, score, node.filename))
        for child in node.children.values():
            if len(output) < length:
                Trie.dfs(child, f"{prefix} {child.word}", score, output, MAX_QUERIES)
            else:
                break

    def search(self, prefix: str, last_word_prefix: str):
        output = []
        sentence_match = True
        node = self.root
        prefix = prefix.lower()
        for word in prefix.split():
            last_node = node
            if word in node.children:
                node = node.children[word]
            else:
                sentence_match = False
        if sentence_match:
            self.dfs(node, prefix, len(prefix) * 2, output, MAX_QUERIES)

        # node = last_node
        if len(output) < MAX_QUERIES:
            self.complete_sentences_from_last_word(node, prefix, last_word_prefix, output)

        if len(output) < MAX_QUERIES:
            self.delete_letter(self.root, prefix, output)
            self.switch_letter(self.root, prefix, output)
            self.insert_letter(self.root, prefix, output)

        return sorted(output, key=lambda x: x[1], reverse=True)

    def complete_sentences_from_last_word(self, node, prefix, last_word_prefix, output):
        for key in node.children.keys():
            if key.startswith(last_word_prefix):
                score = len(prefix) * 2
                self.dfs(node.children[key], f"{prefix.rsplit(' ', 1)[0]} {key}", score, output, MAX_QUERIES)

    def delete_letter(self, root, prefix, output):
        score = len(prefix) * 2
        node = root
        current_prefix = prefix
        found = False
        for i, word in enumerate(current_prefix.split()):
            if word in node.children:
                node = node.children[word]
            else:
                for child in node.children.keys():
                    if len(child) == len(word) - 1:
                        for index in range(len(word)):
                            if child == word[:index] + word[index + 1:]:
                                score -= 2 if index > 3 else (10 - i)
                                found = True
                                node = node.children[child]
                                lst = prefix.split()
                                lst[i] = child
                                prefix = ' '.join([word for word in lst])
                                break
        if found:
            self.dfs(node, prefix, score, output, MAX_QUERIES)

    def switch_letter(self, root, prefix, output):
        score = len(prefix) * 2
        node = root
        current_prefix = prefix
        find_one_correction = False
        for i, word in enumerate(current_prefix.split()):
            if word in node.children:
                node = node.children[word]
            else:
                for child in node.children.keys():
                    if len(child) == len(word):
                        for index in range(len(word)):
                            for letter in string.ascii_lowercase:
                                if child == word[:index] + letter + word[index + 1:] \
                                        and not find_one_correction:
                                    score -= (5 - i) if i < 4 else 1
                                    node = node.children[child]
                                    lst = prefix.split()
                                    lst[i] = child
                                    prefix = ' '.join([word for word in lst])
                                    find_one_correction = True
                                    self.dfs(node, prefix, score, output, MAX_QUERIES)

    def insert_letter(self, root, prefix, output):
        node = root
        score = len(prefix) * 2
        prefix = prefix.lower()
        find_one_correction = False
        for i, word in enumerate(prefix.split()):
            if word in node.children:
                node = node.children[word]
            else:
                for child in node.children.keys():
                    if len(child) == len(word) + 1:
                        for index in range(len(word)):
                            for letter in string.ascii_lowercase:
                                if child == word[:index] + letter + word[index:] and not find_one_correction:
                                    find_one_correction = True
                                    score -= 2 if index > 3 else (10 - i)
                                    node = node.children[child]
                                    lst = prefix.split()
                                    lst[i] = child
                                    prefix = ' '.join([word for word in lst])
                                    continue
        if find_one_correction:
            self.dfs(node, prefix, score, output, MAX_QUERIES)




        # print("last_node: " + last_node.word)
        # print("curr: " + node.word)
        # print(last_word_prefix)