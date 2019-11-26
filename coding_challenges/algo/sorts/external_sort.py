import logging
import math
import os
import shutil
import string
import sys
from contextlib import ExitStack
import random
from functools import wraps


TMP_DIR = '/tmp/ext_sort'
os.makedirs(TMP_DIR, exist_ok=True)
MAX_MERGE = 2
MAX_MEM = 10_000

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger()
        logger.info(
            f'Call {func.__name__} '
            f'With arguments {args} {kwargs}'
        )
        func_res = func(*args, **kwargs)
        logger.info(
            f'Exiting {func.__name__} '
            f'Returned {func_res} {kwargs}'
        )
        return func_res

    return wrapper


def check_end(f):
    return f.tell() == os.fstat(f.fileno()).st_size


def line_or_none(f):
    res = None if check_end(f) else f.readline().strip()
    return res


def get_next_prefix(p):
    return '0' if p == '' else ''


# @logged
def merge_files(*files, out_name):
    if len(files) == 1:
        with open(out_name, 'w') as o:
            l = line_or_none(files[0])
            count = 0
            while l is not None:
                print(l, file=o)
                l = line_or_none(files[0])
                count += 1

            return count

    with open(out_name, 'w') as out_file:
        lines = [line_or_none(f) for f in files]
        count = 0
        while any(l is not None for l in lines):
            min_str = min(filter(lambda l: l is not None, lines))
            ind = lines.index(min_str)
            print(min_str, file=out_file)
            count += 1

            lines[ind] = line_or_none(files[ind])

        return count


@logged
def merge_all_files(n, in_prefix='', out_prefix=''):
    filenames = [in_prefix + str(i) for i in range(1, n + 1)]
    filenames = [os.path.join(TMP_DIR, fname) for fname in filenames]
    out_prefix = os.path.join(TMP_DIR, out_prefix)

    with ExitStack() as stack:
        files = [stack.enter_context(open(fname, 'r+')) for fname in filenames]
        iters = int(math.ceil(len(filenames) / MAX_MERGE))
        count = 0

        for i in range(0, iters):
            min_i = i * MAX_MERGE
            max_i = min((i + 1) * MAX_MERGE, len(files))
            cc = merge_files(*files[min_i:max_i], out_name=out_prefix + str(i+1))
            count += cc

            for file in files[min_i:max_i]:  # remove unneeded files
                os.unlink(file.name)

        print(count)

        return iters


@logged
def merge_until_done(n, in_prefix, res_file):
    current_in_prefix = in_prefix
    while n > 1:
        out_pref = get_next_prefix(current_in_prefix)
        n = merge_all_files(n, in_prefix=current_in_prefix, out_prefix=out_pref)
        current_in_prefix = out_pref

    last = os.path.join(TMP_DIR, current_in_prefix + '1')
    shutil.move(last, res_file)


@logged
def create_chunks(filename, max_size):
    with open(filename, 'r') as f:
        file_num = 0
        current_str = None

        while not check_end(f):
            file_num += 1
            current_size = 0
            with open(os.path.join(TMP_DIR, str(file_num)), 'w') as temp_file:
                res = []
                if current_str is not None:
                    res.append(current_str)
                    current_size += len(current_str)

                current_str = line_or_none(f)
                current_size += len(current_str)

                while current_size < max_size:
                    res.append(current_str)
                    if check_end(f):
                        break
                    current_str = line_or_none(f)
                    current_size += len(current_str)

                print(*sorted(res), file=temp_file, sep='\n')

        return file_num


@logged
def external_sort(file, result, max_size):
    n = create_chunks(file, max_size)
    merge_until_done(n, '', result)


@logged
def create_test_file(name, num_lines, max_len):
    with open(name, 'w') as f:
        for i in range(num_lines):
            ll = random.randint(1, max_len)
            line = ''.join(random.choices(string.ascii_letters, k=ll))
            print(line, end='\n', file=f)


create_test_file('test.txt', 200000, 30)
external_sort('test.txt', 'res.txt', MAX_MEM)
