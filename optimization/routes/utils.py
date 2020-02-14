from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import tsplib95


def plot_tour(points, col="b"):
    """ Рисуем один лепесток """
    plt.scatter(points[:, 0], points[:, 1], s=2, c="r")
    c = list(points) + [points[0]]
    plt.plot(*zip(*c), c=col, linewidth=0.5)


def plot_tours(routes, points, col=None):
    """ Рисуем несколько лепестков """
    for r in routes:
        print(list(r), calc_len(points[r]))
        plot_tour(points[r], col=col)


def build_matrix(points):
    """ Считаем матрицу расстояний """
    n = len(points)
    matrix = np.empty((n, n))
    for i, j in product(range(n), repeat=2):
        matrix[i, j] = np.linalg.norm(points[i] - points[j])
    return matrix


def calc_len(points):
    """ Считаем длину маршрута из точек """
    res = 0
    for i in range(len(points) - 1):
        res += np.linalg.norm(points[i] - points[i + 1])
    return res


def rotate_to_start(route, start):
    """ Прокручиваем маршрут, чтобы он начинался из начала """
    while route[0] != start:
        route = route[1:] + route[:1]
    return route


def parse_solution(res_path):
    """ Парсим файл решения """
    solution = tsplib95.load_solution(res_path)
    return np.array(solution.tours[0])


def dumps_matrix(matrix: np.ndarray, name="route"):
    """ Сохраняем проблему в формате TSPLIB """
    assert len(matrix.shape) == 2 and matrix.shape[0] == matrix.shape[1]

    # матрица -> str разделенная пробелами
    matrix_s = "\n".join(
        " ".join(str(n) for n in row)
        for row in matrix
    )

    res = "\n".join([
        f"NAME: {name}",
        f"TYPE: TSP",
        f"DIMENSION: {len(matrix)}",
        f"EDGE_WEIGHT_TYPE: EXPLICIT",
        f"EDGE_WEIGHT_FORMAT: FULL_MATRIX",
        f"EDGE_WEIGHT_SECTION",
        f"{matrix_s}",
        f"EOF\n",
    ])

    return res


def split_into_tours(nodes, size):
    nodes *= nodes < size

    bounds = np.where(nodes == 0)[0]
    res = [nodes[bounds[-1]:]]
    for i in range(len(bounds) - 1):
        res += [nodes[bounds[i]: bounds[i + 1] + 1]]

    return res
