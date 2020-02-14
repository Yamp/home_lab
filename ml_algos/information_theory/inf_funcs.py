import numpy as np
import scipy as sp
from scipy.stats import norm

EPS = 1e-100


def entropy(x: np.ndarray):
    """
    Aka shannon information
    We are suggesting that x is probability distribution
    Can be calculated as
    >>> -(np.log(x + EPS) * x).sum()
    This is avg amount of information per sample.
    Information of sample is
    >>> np.log(x)
    """
    return sp.stats.entropy(x)


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """
    p - истинное распределение,
    q - подогнанное распределение,
    Насколько длиннее будет средний код (или насколько больше бит для опознания события в среднем нужно затратить)
    чтобы определить события из распределения p, если код составлен по распределению q?

    Матожидание разницы логарифма вероятности q от p

    Can be calculated as
    >>> np.sum((p * np.log(p / (q + EPS) + EPS)))
    """
    return sp.stats.entropy(p, q)


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """
    Metrical modification of LK-divergence
    """
    m = (p + q) / 2
    return (kl_divergence(p, m) + kl_divergence(q, m)) / 2


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """
    p - истинное распределение,
    q - подогнанное распределение,
    returns: Среднее количество бит для опознания события из p, если оптимальный код составлялся для q
    Aka
    >>> return entropy(p) + kl_divergence(p, q)
    """
    return (p * np.log(q + EPS)).sum()


def log_loss(x: np.ndarray, true_res: int) -> float:
    """
    This is actually KL-divergence(True Dist, Softmax)
    """
    return -np.log(x[true_res])


def log_loss_back(x: np.ndarray, true_res: int) -> float:
    """
    This is actually KL-divergence(Softmax, True Dist)
    """
    true_proba = x[true_res]
    return true_proba * np.log(true_proba)


def counts2probas(x: np.ndarray, alpha: float) -> float:
    return (x + alpha) / (x.sum() + len(x) * alpha)


def perplexity(x: np.ndarray):
    """
    :param x: Считаем, что это вектор вероятностей элементов текста
    :return: Оценка вероятности текста нормированная на его длину
    """
    return np.prod(x) ** (1 / len(x))

# TODO: интервальное кодирование с марковской цепью
