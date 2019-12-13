from dataclasses import dataclass
from fractions import Fraction

import numpy as np


@dataclass
class Segment:
    start: Fraction
    width: Fraction


def build_prob(input_codes: bytes):
    unique, counts = np.unique(np.frombuffer(input_codes, dtype='b'), return_counts=True)
    sums = np.cumsum(np.hstack(([0], counts)))

    return {unique[i]: Segment(
        start=Fraction(sums[i], sums[-1]),
        width=Fraction(counts[i], sums[-1]),
    ) for i in range(len(unique))}


def find_fraction_range(data: bytes, probas):
    start, width = Fraction(0), Fraction(1)

    for code in data:
        start += probas[code].start * width
        width *= probas[code].width

    return start, start + width


def find_number(input_start: Fraction, input_end: Fraction) -> int:
    output_fraction = Fraction(0)
    output_denominator = 1

    while not (input_start <= output_fraction < input_end):
        output_numerator = 1 + ((input_start.numerator * output_denominator) // input_start.denominator)
        output_fraction = Fraction(output_numerator, output_denominator)
        output_denominator *= 2

    return output_fraction.numerator


if __name__ == "__main__":
    string = b'BANANAS'
    probas = build_prob(string)
    print(f'{probas=}')
    a, b = find_fraction_range(string, probas)
    num = find_number(a, b)
    print(a, b, num)
