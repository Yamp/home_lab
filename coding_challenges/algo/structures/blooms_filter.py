import math

from BitVector import BitVector


class BloomFilter:
    def __init__(self, max_elements: int, max_error_proba: float):
        self.size = math.log(1 / max_error_proba) / math.log(2) ** 2 * max_elements
        self.size = int(math.ceil(self.size))
        self.table = BitVector(size=self.size)
        self.hashes = int(round(self.size / max_elements * math.log(2)))

    def add(self, obj):
        for h in self._iter_hashes(obj):
            self.table[h] = True

    def check(self, obj):
        for h in self._iter_hashes(obj):
            if not self.table[h]:
                return False

        return True

    def _hash(self, obj, param=0):
        return (hash(obj) + param) % self.size

    def _iter_hashes(self, obj):
        for param in range(self.hashes):
            yield self._hash(obj, param=param)
