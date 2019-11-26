from typing import Union, Tuple

import numpy as np


class BitArray:
    def __init__(self, size: int):
        self.data = np.zeros(size // 64 + 1, dtype=np.int64)

    def __getitem__(self, i: int) -> int:
        return self.data[i // 64] & (1 << (i % 64))

    def __setitem__(self, i: int, bit: Union[int, bool]) -> None:
        self.data[i // 64] = int(self.data[i // 64]) | int(bit << (i % 64))


class BitMatrix:
    def __init__(self, cols: int, rows: int) -> None:
        self.data = np.zeros((cols, rows // 64 + 1))

    def __getitem__(self, indices: Tuple[int, int]) -> int:
        return self.data[indices[0]][indices[1] // 64] & (1 << indices[1] % 64)

    def __setitem__(self, indices: Tuple[int, int], bit: Union[int, bool]) -> None:
        self.data[indices[0]][indices[1] // 64] |= (bit << indices[1] % 64)


if __name__ == "__main__":
    bm = BitArray(1000)
    bm[0] = 1
    bm[2] = 1
    bm[4] = 1
    # bm[62] = 1
    # bm[63] = 1
    # bm[64] = 1
    # bm[65] = 1
    for i in range(1000):
        print(bm[i])
