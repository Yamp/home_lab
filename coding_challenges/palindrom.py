from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    word: str
    neighbours: List
    visited: bool = False
