from dataclasses import dataclass

from typing import List


@dataclass
class KnapsackItem:
    weight: int
    price: float


def knapsack(items: List[KnapsackItem], max_weight: int):
    l = len(items)
    table = [[0.0] * max_weight for k in range(l)]  # table[num][weight]

    # base
    for weight in range(1, max_weight):
        table[0][weight] = float('-inf')

    for weight in range(1, max_weight):
        for num in range(1, l):
            # if items[num].weight
            if weight - items[num].weight > 0:
                table[num][weight] = max(
                    table[num - 1][weight],
                    table[num - 1][weight - items[num].weight] + items[num].price
                )
