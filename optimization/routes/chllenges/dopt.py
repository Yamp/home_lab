import numpy as np
import matplotlib.pyplot as plt


def f_sumdists(Dist, perm):
    """ Расстояние для заданной перестановки """
    return Dist[np.arange(perm.size), perm].sum()


def get_greedy(Dist, init):
    """ Жадный алгоритм коммивояжёра """
    m = Dist.shape[0]

    bag = set(range(m))
    bag.remove(init)
    gperm = np.array(range(m))
    curr = init

    for i in range(m - 1):
        n = min(bag, key=lambda c: Dist[curr, c])  # <<< можно сделать быстрее
        gperm[curr] = n
        curr = n
        bag.remove(n)

    gperm[curr] = init  # замыкание цикла
    return gperm


def run_anneal(f, g_change, perm0, n_steps=100, T0=1.0, T1=0.0):
    """
    f - функция для оптимизации
    g_change - функция изменения текущего решения
    perm0 - начальное решение
    n_steps - число шагов
    T0, T1 - начальная и конечная температуры
    """
    steps = []
    steps_f1 = []
    steps_f2 = []
    a_ = []

    perm = perm0.copy()
    f_old = f(perm)
    for i in range(n_steps):
        # понижение температуры
        T = T0 * (1 - i / n_steps) + T1 * i / n_steps
        # новое решение
        perm_new = g_change(perm)
        # оценить насколько хорошо
        f_new = f(perm_new)
        a = np.exp(-(f_new - f_old) / T)
        # сохраняем по любому
        steps.append(perm)  # не совсем значения соответствуют перестановкам... (только в steps, steps_f1)
        steps_f1.append(f_old)
        steps_f2.append(f_new)
        a_.append(a)
        # смотритм, стоит ли переходить
        if np.random.uniform() <= a:
            perm = perm_new.copy()
            f_old = f_new.copy()
    return steps, steps_f1, steps_f2, a_


def perm2cycle(perm):
    """
    перекодировать перестановку в цикл
    """
    #     n = len(perm)
    #     c = np.zeros(n, dtype='int')
    #     for t in range(1, n): # <<< м.б. можно эффективнее
    #         # print (t, c, c[t], c[t-1])
    #         c[t] = perm[c[t - 1]]
    #     return (c)
    # почему-то так быстрее
    c = [0]
    for _ in range(len(perm) - 1):
        c.append(perm[c[-1]])
    return (np.array(c))


def cycle2perm(c):
    """
    цикл в перестановку
    """
    n = len(c)
    p = np.empty(n, dtype='int')
    for i in range(n - 1):
        p[c[i]] = c[i + 1]
    p[c[-1]] = c[0]
    return p


def rollpart(perm0):
    """
    получить перестановку,
    в которой инвертирован подпуть i -> j
    здесь перестановка кодируется циклом!!!
    """
    n = perm0.size
    perm = np.roll(perm0.copy(), np.random.randint(n))  # перемешиваем
    i = np.random.randint(2, np.ceil(n / 2) + 1)
    perm[:i] = np.flip(perm[:i])

    return perm


def g_change(perm):
    """
    немного изменить перестановку
    получить перестановку,
    в которой инвертирован подпуть i -> j
    """
    return cycle2perm(rollpart(perm2cycle(perm)))


def randomcycle(n):
    """
    случайная перестановка,
    которая соответствует циклу!
    """
    return cycle2perm(np.random.permutation(n))
