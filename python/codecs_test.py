import json
import pickle
import random
from io import BytesIO
from time import time
from timeit import timeit

import blosc
import humanfriendly
import numba
import numpy as np
import hickle as hkl
import rapidjson
import ujson
from bloscpack import pack_ndarray_to_bytes, BloscArgs
from numba import njit
import msgpack
import msgpack_numpy as m

import zlib
import bz2
import lzma
import brotli
import lz4
import lz4.frame as lz4
import zstd
from snappy import snappy

from prettytable import PrettyTable

random_name = 'rnd.npy'
sparse_name = 'spa.npy'
semirandom_name = 'srnd.npy'


@njit(target='cpu')
def semirandomize(arr: np.ndarray):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i][j] = arr[random.randint(0, arr.shape[0] - 1), random.randint(0, arr.shape[1] - 1)]


@njit(target='cpu')
def fill_sparse(arr: np.ndarray, fill_factor=0.3):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if random.random() < 1 - fill_factor:
                arr[i][j] = 0


def create_arrays():
    random_array = np.random.rand(1000, 1000).astype('float32')
    sparse_array = np.random.rand(1000, 1000).astype('float32')
    semirandom_array = np.random.rand(1000, 1000).astype('float32')

    semirandomize(semirandom_array)
    fill_sparse(sparse_array)

    np.save(random_name, random_array)
    np.save(sparse_name, sparse_array)
    np.save(semirandom_name, semirandom_array)


def get_arrays():
    random_array = np.load(random_name)
    sparse_array = np.load(sparse_name)
    semirandom_array = np.load(semirandom_name)

    return random_array, sparse_array, semirandom_array


# create_arrays()
r, s, sr = get_arrays()


def pretty_size(arr: bytes):
    return humanfriendly.format_size(len(arr), binary=True)


def serialize_pickle(arr):
    return pickle.dumps(arr, protocol=pickle.HIGHEST_PROTOCOL)


def serialize_msgpack(arr):
    return msgpack.packb(arr, use_bin_type=True)


def serialize_json(arr: np.ndarray):
    return json.dumps(arr.tolist()).encode(encoding='utf8')


def serialize_ujson(arr: np.ndarray):
    return ujson.dumps(arr.tolist()).encode(encoding='utf8')


def serialize_rjson(arr: np.ndarray):
    return rapidjson.dumps(arr.tolist()).encode(encoding='utf8')


def serialize_bytes(arr: np.ndarray):
    return arr.tobytes()


def serialize_zlib(arr: np.ndarray):
    return zlib.compress(arr.tobytes(), level=1)


def serialize_bz2(arr: np.ndarray):
    return bz2.compress(arr.tobytes(), compresslevel=1)


def serialize_lzma(arr: np.ndarray):  # too long, though good
    return lzma.compress(arr.tobytes(), preset=None)


def serialize_brotli(arr: np.ndarray):
    return brotli.compress(arr.tobytes(), quality=1)


def serialize_snappy(arr: np.ndarray):
    return snappy.compress(arr.tobytes())


def serialize_lz4(arr: np.ndarray):  # slow and stupid
    return lz4.compress(arr.tobytes())


def serialize_zstd(arr: np.ndarray):  # slow and stupid
    return zstd.compress(arr.tobytes(), 4)


def serialize_numpy(arr: np.ndarray):
    stream = BytesIO()
    np.savez(stream, arr)
    return stream.getbuffer()


def serialize_hickle(arr: np.ndarray):
    stream = BytesIO()  # doesnt work
    hkl.dump(arr, stream)
    return stream.getbuffer()


def serialize_(arr: np.ndarray):
    stream = BytesIO()  # doesnt work
    hkl.dump(arr, stream)
    return stream.getbuffer()


def serialize_numpy_compressed(arr: np.ndarray):  # slow and stupid
    stream = BytesIO()
    np.savez_compressed(stream, arr)
    return stream.getbuffer()


def compress_blosc(arr):
    return blosc.pack_array(arr, shuffle=blosc.NOSHUFFLE, cname='zstd', clevel=2)


def compress_blocs_bytes(arr):
    return blosc.compress(arr, shuffle=blosc.NOSHUFFLE, cname='zstd', clevel=2)


def serialize_blosc_lz4(arr: np.ndarray):
    res = blosc.pack_array(arr, shuffle=blosc.BITSHUFFLE, cname='lz4', clevel=2)
    return res


def serialize_csv(arr: np.ndarray):
    stream = BytesIO()
    np.savetxt(stream, arr)
    return stream.getbuffer()


def bench_methods(methods):
    t = PrettyTable(['Method', 'Random', 'Sparse', 'Semirandom', 'Time'])
    for f in methods:
        start_time = time()
        r_size, s_size, sr_size = pretty_size(f(r)), pretty_size(f(s)), pretty_size(f(sr))
        t.add_row([f.__name__, r_size, s_size, sr_size, time() - start_time])
        print(f'{f.__name__} on r {r_size} s {s_size} sr {sr_size}')

    print(t)


# квинтессенция всегоxx
def pack_arrays(a1, a2, a3):
    data = {
        "random": a1,
        "sparse": a2,
        "semisparse": a3
    }

    # blosc.set_nthreads(6)  # Should be number of *REAL* (not virtual) cores. Can bring speedup sometimes.
    blosc.set_releasegil(True)  # Somehow makes things a bit faster
    res = msgpack.packb(data, use_bin_type=True)
    res = blosc.compress(res, cname='zstd', clevel=2)
    return res


def bench_pack():
    res = pack_arrays(r, s, sr)
    print(pretty_size(res))
    t = timeit('pack_arrays(r, s, sr)', globals=globals(), number=500)
    print(t)


# bench_methods([serialize_csv, serialize_ujson, serialize_numpy, serialize_snappy, serialize_blosc_lz4, compress_blosc])

bench_pack()
