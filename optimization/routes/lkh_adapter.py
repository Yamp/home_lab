import numpy as np
import os
import subprocess

from optimization.routes import PROBLEM_FILE
from optimization.routes.utils import parse_solution, dumps_matrix, split_into_tours


def create_lkh_par(tsp_path, par_path, out_path, mtsp=False, vehicles=1, trace_level=1):
    """ Создаем файл с параметрами для запуска LKH """

    par = ''
    par += 'SPECIAL\n' * mtsp
    par += f'PROBLEM_FILE = {tsp_path}\n'
    par += f'TOUR_FILE = {out_path}\n'
    par += f'VEHICLES = {vehicles}\n' * mtsp
    par += f'MTSP_OBJECTIVE = MINMAX\n' * mtsp
    par += f'DEPOT = 1\n' * mtsp
    par += f'INITIAL_TOUR_ALGORITHM = MTSP\n' * mtsp
    par += f'TRACE_LEVEL = {trace_level}'

    with open(par_path, "w") as dest:
        dest.write(par)


def run_lkh(par_path, out_path):
    """ Запускаем LKH-решалку """

    LKH = os.environ.get("LKH", "LKH")  # LKH
    output = subprocess.check_output([LKH, par_path], shell=False)

    return parse_solution(out_path), output


def solve_lkh(matrix, mtsp=False, vehicles=1, trace_level=1):
    """ Интерфейс к LKH-3 """
    mtsp = vehicles != 1 and mtsp

    mult = 16777216 / matrix.max()  # масштабируем матрицу, чтобы минимизировать потери
    matrix = (mult * matrix).astype("int32")

    # всякие пути к файлам
    tsp_path = os.path.abspath(PROBLEM_FILE)  # абсолютный путь к файлу с задачей
    par_path = f'{os.path.splitext(tsp_path)[0]}.par'  # файл с параметрами
    out_path = f'{os.path.splitext(tsp_path)[0]}.sol'  # файл с результатом

    with open(tsp_path, "w") as dest:  # записываем задачу
        dest.write(dumps_matrix(matrix, name="My Route"))

    create_lkh_par(  # записываем файл параметров
        tsp_path, par_path, out_path,
        mtsp=mtsp, vehicles=vehicles, trace_level=trace_level
    )

    tour, meta = run_lkh(par_path, out_path)
    tour = split_into_tours(tour - 1, len(matrix))   # приводим к 0-индексам и делим на маршруты

    return tour, meta
