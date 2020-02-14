import math

import numpy as np
from numba import jit, njit
from typing import List, Tuple, Iterable, Collection, Container, Sequence

import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import tensorflow as tf
import seaborn as sns
import scipy as sp


# ------------------------------ activation functions ---------------------------------------------

@njit(parallel=True)
def tanh(x: np.ndarray):
    # a, b = np.exp(x), np.exp(-x)
    # return (a - b) / (a + b)
    return np.tanh(x)


@njit(parallel=True)
def logistic(x: np.ndarray):
    e = np.exp(-x)
    return e / (1 + e)


@njit(parallel=True)
def relu(x: np.ndarray):
    return x * (x > 0)


def generalized_relu(x: np.ndarray, alpha: float):
    return np.maximum(0, x) + alpha * np.minimum(0, x)


def abs_relu(x: np.ndarray):
    return np.abs(x)


def maxout(x: np.ndarray, w1, w2, b1, b2):
    return max(np.dot(x, w1) + b1, np.dot(x, w2) + b2)


def maxout_max(x: np.ndarray):
    return np.max(x)


def smooth_relu(x: np.ndarray):
    return np.log(1 + np.exp(x))


def softmax(x: np.ndarray):
    return (a := np.exp(x)) / a.sum()


def linear(x: np.ndarray):
    """
    Good for regression tasks
    """
    return x


# --------------------------------- Metrics -----------------------------------------------------

def mse(y_pred: np.ndarray, y_true: np.ndarray):
    return (y_pred - y_true).mean()


def cross_entropy(y_pred: np.ndarray, y_true: np.ndarray):
    """
    Логарифм правдоподобия
    """
    return (y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()


# ------------------------------- Инициализация -------------------------------------------------

def weights(inputs: int, outputs: int, size: int, method='1'):
    if method == '1':
        bound = 1 / math.sqrt(inputs)
        return np.random.uniform(-bound, bound, size=size)

    if method == '2':
        bound = 6 / math.sqrt(inputs + outputs)
        return np.random.uniform(-bound, bound, size=size)


def init_softmax(classes_probas: np.ndarray):
    # softmax(res) == classes_proba
    # return res
    ...


class Perceptron:
    def __init__(self, layers: Sequence[int]):
        self.layers = [
            np.zeros(layers[i] + 1, layers[i + 1])  # + 1 for === 1 input
            for i in range(len(layers))
        ]
        self.activation = logistic

    def initialize(self):
        for l in self.layers:
            l[:] = np.random.rand(l.shape)
            l[0, :] = 1

    def predict(self, x: np.ndarray):
        current = x
        for l in self.layers:
            current = self.activation(current)
            current = np.hstack((1, l @ current))

        return current
