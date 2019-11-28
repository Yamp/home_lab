from dataclasses import dataclass

import numpy as np


@dataclass
class LinerProblem:
    A_lb: np.ndarray
    A_ub: np.ndarray
    A_eq: np.ndarray

    b_lb: np.ndarray
    b_ub: np.ndarray
    b_eq: np.ndarray

    objective = np.ndarray

    is_maximization: bool = True

    def to_maximization(self):
        """ Turning problem to maximization problem """
        if not self.is_maximization:
            self.objective = -self.objective
            self.is_maximization = True

    def lb2ub(self):
        """
        [Ax >= b] -> [-Ax <= -b]
        """
        self.A_ub = np.vstack((
            self.A_ub,
            -self.A_lb,
        ))
        self.b_ub = np.vstack((
            self.b_ub,
            -self.b_lb,
        ))

        del self.A_lb, self.b_lb

    def eq2ub(self):
        """
        [Ax == b] -> [Ax <= b and Ax >= b]
        """
        self.A_ub = np.vstack((
            self.A_ub,
            self.A_eq,
            -self.A_eq,
        ))
        self.b_ub = np.vstack((
            self.b_ub,
            self.b_eq,
            self.b_eq,
        ))

        del self.A_eq, self.b_eq

    def add_nonnegativity(self):
        """
        We are adding a pair of variables for each var like x = x' - x''
        [Ax <= b] -> [(A)(-A)x <= b]
        cx -> (c)(-c)x
        """
        self.objective = np.hstack((self.objective, -self.objective))
        self.A_ub = np.hstack((self.A_ub, -self.A_ub))

    def to_standard_form(self):
        self.to_maximization()
        self.eq2ub()
        self.lb2ub()
        self.add_nonnegativity()

    def to_slack_form(self):
        constr_num = len(self.A_ub)
        self.A_eq = np.hstack(
            (
                -self.A_ub, np.eye(constr_num),
                np.zeros((constr_num, 1))  # this guy is for objective slack
            )
        )

        self.b_eq = np.vstack((
            self.b_ub,
            np.zeros((constr_num, 1)),
            [1]
        ))

        del self.A_ub, self.b_ub

    def pivot(self):
        # finding first nonnull variable
        for i, v in enumerate(self.objective):
            if v < 0:
                var_num = i
                break
        else:
            return True

        # getting tightest constraint
        tightest = np.argmin(
            expr[var_num] / bound for expr, bound
            in zip(self.A_eq, self.b_eq)
        )

        # making pivot variable coefficient == 1
        self.A_eq[tightest] /= self.A_eq[tightest][var_num]
        self.b_eq[tightest] /= self.A_eq[tightest][var_num]

        # making substitution of a
        for i in range(len(self.A_eq)):
            if i != tightest:
                self.A_eq[i] -= self.A_eq[tightest] * self.A_eq[i][var_num]

        self.objective -= self.A_eq[tightest] * self.objective[var_num]
