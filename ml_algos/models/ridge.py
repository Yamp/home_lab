import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# cp.sum_squares(A * x - b)
from ml_algos.neural.test import logistic

loss_fn = lambda X, Y, beta: cp.pnorm(cp.matmul(X, beta) - Y, p=2) ** 2  # суммарный квадрат ошибки
regularizer = lambda beta: cp.pnorm(beta, p=2) ** 2  # сумма квадратов коэффициентов
mse = lambda X, Y, beta: loss_fn(X, Y, beta).value / X.shape[0]  # средний квадрат ошибки

objective_fn = lambda X, Y, beta, lambd: loss_fn(X, Y, beta) + lambd * regularizer(beta)  # что оптимизируем


def generate_regression_data(m: int, n: int, sigma: float):
    beta_star = np.random.randn(n)  # генерируем данные для регрессии
    X = np.random.randn(m, n)  # генерируем плохообусловленную матрицу
    Y = X.dot(beta_star) + np.random.normal(0, sigma, size=m)  # добавляем шум
    return X, Y


def generate_classification_data(m: int, n: int):
    beta_true = np.array([1, 0.5, -0.5] + [0] * (n - 3))
    X = (np.random.random((m, n)) - 0.5) * 10
    Y = np.round(logistic(X @ beta_true + np.random.randn(m) * 0.5))

    return X, Y


def test_train_split(X, Y, train_proportion=0.5):
    assert np.shape(X)[0] == np.shape(Y)[0]
    frac = int(np.shape(Y)[0] * train_proportion)

    X_train, Y_train = X[:frac, :], Y[:frac]
    X_test, Y_test = X[frac:, :], Y[frac:]

    return X_train, Y_train, X_test, Y_test


def optimize_logistic_regression(X, Y):
    beta = cp.Variable(n)
    lambd = cp.Parameter(nonneg=True)
    log_likelihood = cp.sum(
        cp.multiply(Y, X @ beta) - cp.logistic(X @ beta)
    )
    problem = cp.Problem(cp.Maximize(log_likelihood / n - lambd * cp.norm(beta, 1)))
    return problem


def plot_train_test_errors(train_errors, test_errors, lambd_values):
    plt.plot(lambd_values, train_errors, label="Train error")
    plt.plot(lambd_values, test_errors, label="Test error")
    plt.xscale("log")
    plt.legend(loc="upper left")
    plt.xlabel(r"$\lambda$", fontsize=16)
    plt.title("Mean Squared Error (MSE)")
    plt.show()


def plot_regularization_path(lambd_values, beta_values):
    num_coeffs = len(beta_values[0])
    for i in range(num_coeffs):
        plt.plot(lambd_values, [wi[i] for wi in beta_values])
    plt.xlabel(r"$\lambda$", fontsize=16)
    plt.xscale("log")
    plt.title("Regularization Path")
    plt.show()


def errors():
    ...


def accuracy(scores: np.ndarray, labels: np.ndarray) -> float:
    errors = (scores > 0) - labels
    return (errors ** 2).sum() / len(labels)


m, n, sigma = 100, 20, 5

X, Y = generate_regression_data(m, n, sigma)
X_train, Y_train, X_test, Y_test = test_train_split(X, Y, train_proportion=0.5)

beta = cp.Variable(n)
lambd = cp.Parameter(nonneg=True)
problem = cp.Problem(cp.Minimize(objective_fn(X_train, Y_train, beta, lambd)))

lambd_values = np.logspace(-2, 3, 50)
train_errors, test_errors, beta_values = [], [], []

for l in lambd_values:
    lambd.value = l
    problem.solve_tsp()

    train_errors += [mse(X_train, Y_train, beta)]
    test_errors += [mse(X_test, Y_test, beta)]
    beta_values += [beta.value]

plot_train_test_errors(train_errors, test_errors, lambd_values)
plot_regularization_path(lambd_values, beta_values)
