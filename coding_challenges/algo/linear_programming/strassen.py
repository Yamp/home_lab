from typing import Tuple

import numpy as np


def check_matrix_sizes(
        A: np.ndarray, B: np.ndarray, res: np.ndarray
) -> Tuple[int, int, int]:
    """
    A = n * common
    B = common * m
    """
    n = A.shape[0]
    m = B.shape[1]
    common = A.shape[1]

    assert A.shape[1] == B.shape[0], f"Size mismatch {A.shape[1]} != {B.shape[0]}"
    assert res.shape == (n, m), f"Result size mismatch {res.shape} != {(n, m)}"

    return n, m, common


def naive_matrix_multiplication(
        A: np.ndarray, B: np.ndarray, res: np.ndarray
) -> None:
    """
    A = n * common
    B = common * m
    """
    n, m, common = check_matrix_sizes(A, B, res)

    for i in range(n):
        for j in range(m):
            for k in range(common):
                res[i][j] += A[i][k] * B[k][j]


def transpose_matrix_multiplication(
        A: np.ndarray, B: np.ndarray, res: np.ndarray
) -> None:
    """
    A = n * common
    B = common * m
    """
    n, m, common = check_matrix_sizes(A, B, res)

    B = B.T.copy()
    for i in range(n):
        for j in range(m):
            for k in range(common):
                res[i][j] += A[i][k] * B[j][k]


def change_order_matrix_multiplication(
        A: np.ndarray, B: np.ndarray, res: np.ndarray
) -> None:
    """
    A = n * common
    B = common * m
    """
    n, m, common = check_matrix_sizes(A, B, res)

    for i in range(n):
        for k in range(common):
            for j in range(m):
                res[i][j] += A[i][k] * B[k][j]


def strassen_maxtrix_multiplication(
        A: np.ndarray, B: np.ndarray, res: np.ndarray
) -> None:
    """
    A = n * common
    B = common * m
    res = n * m
    """
    n, m, common = check_matrix_sizes(A, B, res)
    n_mid = n // 2
    m_mid = m // 2
    com_mid = common // 2

    A11 = A[:n_mid, :com_mid]
    A12 = A[:n_mid, com_mid:]
    A21 = A[n_mid:, :com_mid]
    A22 = A[n_mid:, com_mid:]

    B11 = B[:com_mid, :m_mid]
    B12 = B[:com_mid, m_mid:]
    B21 = B[com_mid:, :m_mid]
    B22 = B[com_mid:, m_mid:]

    C11 = res[:n_mid, :m_mid]
    C12 = res[:n_mid, m_mid:]
    C21 = res[n_mid:, :m_mid]
    C22 = res[n_mid:, m_mid:]

    # (!!!) actually need to go recursive, and add some naive mults for low dim
    M1 = (A11 + A22) @ (B11 + B22)
    M2 = (A21 + A22) @ B11
    M3 = A11 @ (B12 - B22)
    M4 = A22 @ (B21 - B11)
    M5 = (A11 + A12) @ B22
    M6 = (A21 - A11) @ (B11 + B12)
    M7 = (A12 - A22) @ (B21 + B22)

    C11 += M1 + M4 - M5 + M7
    C12 += M3 + M5
    C21 += M2 + M4
    C22 += M1 - M2 + M3 + M6


if __name__ == "__main__":
    n, m, common = 16, 16, 16
    A = np.random.randint(100, size=(n, common))
    B = np.random.randint(100, size=(common, m))
    true_res = A @ B

    print(f'{A.shape=}, {B.shape=}, {true_res.shape=}')

    res = np.zeros((n, m), dtype=np.int)
    naive_matrix_multiplication(A, B, res)
    print(np.allclose(res, true_res))

    res = np.zeros((n, m), dtype=np.int)
    transpose_matrix_multiplication(A, B, res)
    print(np.allclose(res, true_res))

    res = np.zeros((n, m), dtype=np.int)
    change_order_matrix_multiplication(A, B, res)
    print(np.allclose(res, true_res))

    res = np.zeros((n, m), dtype=np.int)
    strassen_maxtrix_multiplication(A, B, res)
    print(np.allclose(res, true_res))
