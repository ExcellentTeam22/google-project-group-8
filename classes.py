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

    def insert(self, line, filename):
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

    def dfs(self, node: TrieNode, prefix: str):
        if node.is_end:
            self.output.append((prefix, node.counter, node.filename))
        for child in node.children.values():
            self.dfs(child, f"{prefix} {child.word}")

    def search(self, prefix: str, last_word_prefix: str):
        completed_words = True
        self.output = []
        node = self.root
        for word in prefix.split():
            word = str(word).lower()
            if word in node.children:
                node = node.children[word]
            else:
                list_of_children = []
                found_word_contains_last_word_pref = False
                for wordd, nodee in node.children.items():
                    if str(wordd).startswith(last_word_prefix):
                        found_word_contains_last_word_pref = True
                        completed_words = False
                        list_of_children.append(nodee)
                        # node = node.children[wordd]
                if not found_word_contains_last_word_pref:
                    return []  # here we need to delete/insert/replace a character

        prefix = prefix if completed_words else prefix.rsplit(' ', 1)[0]
        if not completed_words:
            for n in list_of_children:
                self.dfs(n, prefix + ' ' + n.word)
        else:
            self.dfs(node, prefix)

        # prefix = prefix if completed_words else prefix.rsplit(' ', 1)[0]
        # self.dfs(node, prefix)
        # if len(self.output) < MAX_QUERIES:
        return sorted(self.output, key=lambda x: x[1], reverse=True)