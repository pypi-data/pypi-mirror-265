import numpy as np
import sympy

from copul.families.archimedean import Nelsen3


class Checkerboarder:
    def __init__(self, checkerboard_size=10):
        self.checkerboard_size = checkerboard_size

    def compute_check_copula(self, copula):
        n = self.checkerboard_size
        cdf = copula.cdf.func
        checkerboard_matrix = sympy.Matrix.zeros(n)
        for i, j in np.ndindex(n, n):
            if i == 0:
                if j == 0:
                    checkerboard_matrix[i, j] = cdf.subs(copula.u, 1 / n).subs(copula.v, 1 / n)
                else:
                    checkerboard_matrix[i, j] = cdf.subs(copula.u, 1 / n).subs(
                        copula.v, (j + 1) / n
                    ) - cdf.subs(copula.u, 1 / n).subs(copula.v, j / n)
            elif j == 0:
                checkerboard_matrix[i, j] = cdf.subs(copula.u, (i + 1) / n).subs(
                    copula.v, 1 / n
                ) - cdf.subs(copula.u, i / n).subs(copula.v, 1 / n)
            else:
                checkerboard_matrix[i, j] = (
                    cdf.subs(copula.u, (i + 1) / n).subs(copula.v, (j + 1) / n)
                    + cdf.subs(copula.u, i / n).subs(copula.v, j / n)
                    - cdf.subs(copula.u, i / n).subs(copula.v, (j + 1) / n)
                    - cdf.subs(copula.u, (i + 1) / n).subs(copula.v, j / n)
                )
        return checkerboard_matrix


if __name__ == "__main__":
    copula = Nelsen3(theta=0.5)
    checkerboarder = Checkerboarder(3)
    matrix = checkerboarder.compute_check_copula(copula)
    print("Done!")
