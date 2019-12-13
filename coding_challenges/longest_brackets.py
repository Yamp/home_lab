import re

repeats = re.compile(r'(\w)\1*')
numbers = set('1234567890')
letters = set('qwertyuiopasdfghjklzxcvbnm')
upper_letters = set('QWERTYUIOPASDFGHJKLZXCVBNM')
repeat_groups = None


def check_strong(s: str) -> bool:
    global repeat_groups
    s_set = set(s)
    repeat_groups = [match.group() for match in repeats.finditer(s)]

    factors = (
        6 <= len(s) <= 20,
        len(numbers & s_set) != 0,
        len(letters & s_set) != 0,
        len(upper_letters & s_set) != 0,
        all(len(r) < 3 for r in repeat_groups),
    )

    return all(factors)


def number_of_deletions(s):
    if len(s) > 20:
        return len(s) - 20
    else:
        return 0


def replaces_to_fix_groups():
    return sum(len(g) // 3 for g in repeat_groups)


def inserts_to_fix_groups():
    return sum((len(g) - 1) // 2 for g in repeat_groups)


def need_number_or_deletions(s):
    print(s)


# необходимо и достаточно по 1 (вставке или замене) на каждый отсутствующий тип символов

def diff_if_len_is_ok(s):
    s_set = set(s)
    factors = (
        len(numbers & s_set) != 0,
        len(letters & s_set) != 0,
        len(upper_letters & s_set) != 0,
    )

    min_change1 = sum(factors)
    min_change2 = replaces_to_fix_groups()
    return max(min_change1, min_change2)


def diff_if_len_too_small(s):
    s_set = set(s)
    factors = (
        len(numbers & s_set) != 0,
        len(letters & s_set) != 0,
        len(upper_letters & s_set) != 0,
    )

    min_change1 = 6 - len(s)
    min_change2 = inserts_to_fix_groups()
    min_change3 = sum(factors)

    inserts = max(min_change1, min_change3)

    return max(min_change1, min_change2, min_change3)


class Solution:
    def strongPasswordChecker(self, s: str) -> int:
        ...
