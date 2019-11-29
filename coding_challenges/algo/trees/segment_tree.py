import numpy as np


class SegmentTree:
    def __init__(self, data):
        self.tree = np.array(len(data) * 2)  # multiplying by 2 for corner cases
        self._build_tree(data, 0, len(data) - 1, 0)

    def _build_tree(
            self, data,
            first: int, last: int,
            res_num: int
    ) -> None:
        if first == last:
            self.tree[res_num] = data[first]
            return

        middle = (first + last) // 2
        self._build_tree(data, first, middle, res_num * 2 + 1)  # trying to stay zero-indexed
        self._build_tree(data, middle + 1, last, res_num * 2 + 2)

        self.tree[res_num] = self.tree[res_num * 2 + 1] + self.tree[res_num * 2 + 2]

    def sum(
            self,
            first: int, last: int,
            domain_first: int, domain_last: int,
            sum_ind: int
    ) -> int:
        if first > last:
            return 0

        if first == domain_first and last == domain_last:
            return self.tree[sum_ind]

        domain_middle = (domain_first + domain_last) // 2
        return self.sum(
            first, min(last, domain_middle),
            domain_first, domain_middle,
            sum_ind * 2 + 1
        ) + self.sum(
            max(first, domain_middle + 1), last,
            domain_middle + 1, domain_last,
            sum_ind
        )

    def update(
            self, first: int, last: int,
            ind: int, val: int,
            node_ind: int
    ) -> None:
        # TODO: can easily avoid recursion
        if first == last:
            self.tree[node_ind] = val
            return

        middle = (first + last) // 2
        if ind <= middle:
            self.update(
                first, middle,
                ind, val,
                node_ind * 2 + 1
            )
        else:
            self.update(
                middle + 1, last,
                ind, val,
                node_ind * 2 + 1
            )
        self.tree[node_ind] = self.tree[node_ind * 2 + 1] + self.tree[node_ind * 2 + 2]
