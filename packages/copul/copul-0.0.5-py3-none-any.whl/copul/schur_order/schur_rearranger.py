import copy

import numpy as np
import sympy

from copul.schur_order.checkerboarder import Checkerboarder


class SchurRearranger:
    def __init__(self, checkerboard_size=None):
        self._checkerboard_size = checkerboard_size

    def __str__(self):
        return f"SchurRearranger(checkerboard_size={self._checkerboard_size})"

    def rearrange_copula(self, copula):
        checkerboarder = Checkerboarder(self._checkerboard_size)
        ccop = checkerboarder.compute_check_copula(copula)
        return self.rearrange_checkerboard(ccop)

    @staticmethod
    def rearrange_checkerboard(matr):
        if isinstance(matr, list):
            matr = np.array(matr)
        matr = matr.shape[0] * matr.shape[1] * matr / sum(matr)
        B = sympy.Matrix.zeros(matr.shape[0])
        for k, l in np.ndindex(matr.shape):
            B[k, l] = sum(matr[k, j] for j in range(l + 1))
        B = B.col_insert(0, sympy.Matrix([0] * matr.shape[0]))
        B_tilde = sympy.Matrix.zeros(B.shape[0], B.shape[1])
        for l_ in range(B.shape[1]):
            B_tilde.col_del(l_)
            B_tilde = B_tilde.col_insert(l_, sympy.Matrix(sorted(B.col(l_), reverse=True)))
        a_arrow = sympy.Matrix.zeros(matr.shape[0])
        for k, l in np.ndindex(matr.shape):
            a_arrow[k, l] = B_tilde[k, l + 1] - B_tilde[k, l]
        a_arrow_final = copy.copy(a_arrow)
        return a_arrow_final / (matr.shape[0] * matr.shape[1])
