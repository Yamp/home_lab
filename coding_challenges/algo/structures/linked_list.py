from typing import Optional


# TODO: bloom filter
# TODO: consistent hashing

class LinkedListNode:
    def __inti__(self):
        pass


class LinkedList:
    def __init__(self):
        self.data = None
        self.next: Optional['LinkedList'] = None
        self.prev: Optional['LinkedList'] = None

        self.first: Optional['LinkedList']
        self.last: Optional['LinkedList']

    def push_bash(self, data):
        pass
