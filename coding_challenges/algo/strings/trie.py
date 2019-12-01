from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional


@dataclass
class TrieNode:
    string: str
    is_terminal: bool = False
    children: Mapping['TrieNode'] = field(default_factory=dict)
    fail_link: Optional['TrieNode'] = None


@dataclass
class FirstNode:
    children: Dict['TrieNode'] = field(default_factory=dict)


class Trie:
    def __init__(self, strings):
        self.node = FirstNode()
        self.build_trie(strings)

    def add_str(self, s):
        current_node = self.node
        for c in s:
            if c not in current_node.children:
                current_node.children[c] = TrieNode(c)
                current_node = current_node.children[c]

        current_node.is_terminal = True

    def build_trie(self, strings):
        for s in strings:
            self.add_str(s)

    def build_links(self):
        ...
        # prefix function, but in dfs from trie

    def find_all(self):
        ...

    def find_first(self):
        ...

    def count_all(self):
        ...
