import numpy as np
import sympy

from cop.copul import basictools
from copul.families.abstract_copula import AbstractCopula


class CheckerboardCopula(AbstractCopula):
    params = []
    intervals = {}

    def __init__(self, matr, **kwargs):
        if isinstance(matr, (list, sympy.matrices.dense.Matrix)):
            matr = np.array(matr)
        self.matr = matr
        self.n = matr.shape[0]
        super().__init__(**kwargs)

    def __str__(self):
        return f"CheckerboardCopula(n={self.n})"

    @property
    def is_symmetric(self) -> bool:
        if self.matr.shape[0] != self.matr.shape[1]:
            return False
        return np.allclose(self.matr, self.matr.T)

    @property
    def is_absolutely_continuous(self) -> bool:
        return True

    def cdf(self, u, v):
        subsquare_size = 1.0 / self.n
        total_integral = 0.0

        for i in range(self.n):
            for j in range(self.n):
                # Determine the bottom-left corner of the subsquare
                x, y = i * subsquare_size, j * subsquare_size

                # Determine the top-right corner of the subsquare
                x_next, y_next = (i + 1) * subsquare_size, (j + 1) * subsquare_size

                # Check if the subsquare is completely inside [0, u] x [0, v]
                if x_next <= u and y_next <= v:
                    total_integral += self.matr[i, j] * subsquare_size * subsquare_size
                # Check if the subsquare is partially inside
                elif x < u and y < v:
                    overlap_x = min(u, x_next) - x
                    overlap_y = min(v, y_next) - y
                    total_integral += self.matr[i, j] * overlap_x * overlap_y

        return total_integral * self.n

    def cond_distr_1(self, u, v):
        if isinstance(u, np.ndarray):
            return np.array([self.cond_distr_1(u_, v) for u_ in u])
        subsquare_size = 1.0 / self.n
        total_integral = 0.0

        for i in range(self.n):
            x = i * subsquare_size
            x_next = (i + 1) * subsquare_size
            if not (x <= u < x_next):
                continue
            for j in range(self.n):
                # Determine the bottom-left corner of the subsquare
                y = j * subsquare_size

                # Determine the top-right corner of the subsquare
                y_next = (j + 1) * subsquare_size

                # Check if the subsquare is completely inside [0, u] x [0, v]
                if y_next <= v:
                    total_integral += self.matr[i, j] * subsquare_size
                # Check if the subsquare is partially inside
                elif y < v:
                    overlap_y = min(v, y_next) - y
                    total_integral += self.matr[i, j] * overlap_y
            full_row_sum = sum(self.matr[i, j] * subsquare_size for j in range(self.n))
            return total_integral / full_row_sum

    def cond_distr_2(self, u, v):
        if isinstance(v, np.ndarray):
            return np.array([self.cond_distr_2(u, v_) for v_ in v])
        subsquare_size = 1.0 / self.n
        total_integral = 0.0

        for j in range(self.n):
            y = j * subsquare_size
            y_next = (j + 1) * subsquare_size
            if not (y <= v < y_next):
                continue
            for i in range(self.n):
                # Determine the bottom-left corner of the subsquare
                x = i * subsquare_size

                # Determine the top-right corner of the subsquare
                x_next = (i + 1) * subsquare_size

                # Check if the subsquare is completely inside [0, u] x [0, v]
                if x_next <= u:
                    total_integral += self.matr[i, j] * subsquare_size
                # Check if the subsquare is partially inside
                elif x < u:
                    overlap_x = min(u, x_next) - x
                    total_integral += self.matr[i, j] * overlap_x
            full_col_sum = sum(self.matr[i, j] * subsquare_size for i in range(self.n))
            return total_integral / full_col_sum

    def pdf(self, u, v):
        subsquare_size = 1.0 / self.n
        matrix_sum = sum(self.matr[i, j] for i in range(self.n) for j in range(self.n))

        for i in range(self.n):
            for j in range(self.n):
                # Determine the bottom-left corner of the subsquare
                x, y = i * subsquare_size, j * subsquare_size

                # Determine the top-right corner of the subsquare
                x_next, y_next = (i + 1) * subsquare_size, (j + 1) * subsquare_size

                # Check if the subsquare is partially inside
                if x <= u <= x_next and y <= v <= y_next:
                    return self.matr[i, j] / matrix_sum * self.n**2

    def tau(self):
        result = basictools.monte_carlo_integral(
            lambda x, y: self.cdf(x, y) * self.pdf(x, y)
        )
        return 4 * result - 1

    def rho(self):
        result = basictools.monte_carlo_integral(lambda x, y: self.cdf(x, y))
        return 12 * result - 3

    def xi(self):
        result = basictools.monte_carlo_integral(
            lambda x, y: self.cond_distr_1(x, y) ** 2
        )
        return 6 * result - 2
