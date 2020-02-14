import os
import subprocess

from optimization.routes import PROBLEM_FILE
from optimization.routes.utils import dumps_matrix, rotate_to_start


def run_concorde(tsp_path):
    CONCORDE = os.environ.get("CONCORDE", "concorde")  # получаем concorde
    os.chdir("/tmp/")

    tsp_path = os.path.abspath(tsp_path)  # абсолютный путь
    res_path = f'{os.path.splitext(tsp_path)[0]}.sol'  # тут будет результат

    output = subprocess.check_output([CONCORDE, tsp_path], shell=False)  # запускаем
    output = str(output).strip()  # очищаем output от мусора

    with open(res_path) as f:  # считываем итоговый маршрут
        data = f.read()
        tour = [int(x) for x in data.split()[1:]]

    rotate_to_start(tour, start=0)

    return [tour], output


def solve_concorde(matrix):
    mult = 32767 / matrix.max()
    matrix = (mult * matrix).astype("int32")
    with open(PROBLEM_FILE, "w") as dest:
        dest.write(dumps_matrix(matrix, name="My Route"))
    return run_concorde(PROBLEM_FILE)
