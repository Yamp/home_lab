from io import StringIO


def counter(start: int):
    while True:
        yield start
        start += 1


def compress(data: str):
    """Compress a string to a list of output symbols."""
    dictionary, res = {chr(i): chr(i) for i in range(256)}, []
    cur_char, code_gen = 0, counter(256)

    while cur_char < len(data):
        pref_in_dict = ''  # find largest prefix in dict
        while cur_char < len(data) and (new_pref := pref_in_dict + data[cur_char]) in dictionary:
            pref_in_dict = new_pref
            cur_char += 1

        res += [dictionary[pref_in_dict]]  # write it as code, add next pref to dict
        dictionary[new_pref] = next(code_gen)

    return res


def decompress(compressed):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = compressed.pop(0)
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()


# How to use:
compressed = compress('TOBEORNOTTOBEORTOBEORNOT')
print(compressed)
decompressed = decompress(compressed)
print(decompressed)
