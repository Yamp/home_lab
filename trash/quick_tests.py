#!/bin/python3

import math
import os
import random
import re
import sys
import pickle


def read_data_from_single_string(joined_string):
    """
    Use this function to read the string in the input file
    """
    ordered_keys = ['closes', 'positions', 'currency_mapping', 'fx_rates']
    hex_strings = joined_string.split()
    assert len(ordered_keys) == len(hex_strings)  # If not, data is malformed
    data = {}
    for i, k in enumerate(ordered_keys):
        data[k] = pickle.loads(bytes.fromhex(hex_strings[i]))

    return data


def calculate_pnl(closes, positions, currency_mapping, fx_rates):
    """
    Parameters
    ----------
    closes : dict
        Prices of the instruments, format (date_str, ticker) : value
    positions : dict
        Positions entered, format (date_str, ticker) : value
    currency_mapping : list
        Currency mapping, format (ticker, currency_name)
    fx_rates : dict
        Currency rates for desired dates

    Returns
    -------
    float
        total profit (loss if negative) experienced by this position table, rounded to cents
    """

    # #1 priority is test case completion, #2 is code readability gauged by an actual person reading it.
    # Please don't dwell on performance-related stuff, not the proper environment to do that.

    def get_usd_price(ticker, date_str):
        fx_rates[date_str] = ""

    result = ...
    return result


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    no_of_lines = 4
    joined_string = ""
    for i in range(no_of_lines):
        joined_string += input() + "\n"

    data = read_data_from_single_string(joined_string)

    result = calculate_pnl(data['closes'], data['positions'], data['currency_mapping'], data['fx_rates'])

    fptr.write(str(round(result, 2)))

    fptr.close()
