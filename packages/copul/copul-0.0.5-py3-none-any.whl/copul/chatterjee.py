import numpy as np
from scipy import stats


def xi_ncalculate(xvec, yvec):
    n = len(xvec)
    xrank = stats.rankdata(xvec, method="ordinal")
    yrank = stats.rankdata(yvec, method="ordinal")
    ord_ = np.argsort(xrank)
    yrank = yrank[ord_]
    coef_sum = np.sum(np.abs(yrank[1:n] - yrank[: n - 1]))
    return 1 - 3 * coef_sum / (n**2 - 1)


def xi_nvarcalculate(xvec, yvec):
    n = len(xvec)
    xrank = np.argsort(np.argsort(xvec)) + 1
    yrank_temp = np.argsort(np.argsort(yvec)) + 1
    ord_ = np.argsort(xrank)
    yrank = yrank_temp[ord_]
    yrank1 = np.concatenate((yrank[1:n], [yrank[n - 1]]))
    yrank2 = np.concatenate((yrank[2:n], [yrank[n - 1]] * 2))
    yrank3 = np.concatenate((yrank[3:n], [yrank[n - 1]] * 3))
    term1 = np.minimum(yrank, yrank1)
    term2 = np.minimum(yrank, yrank2)
    term3 = np.minimum(yrank2, yrank3)
    term4 = np.array([np.sum(yrank[i] <= term1[np.arange(n) != i]) for i in range(n)])
    term5 = np.minimum(yrank1, yrank2)
    sum1 = np.mean((term1 / n) ** 2)
    sum2 = np.mean(term1 * term2 / n**2)
    sum3 = np.mean(term1 * term3 / n**2)
    sum4 = np.mean(term4 * term1 / (n * (n - 1)))
    sum5 = np.mean(term4 * term5 / (n * (n - 1)))
    sum6 = np.mean(
        np.array([np.sum(np.minimum(term1[i], term1[np.arange(n) != i])) for i in range(n)])
        / (n * (n - 1))
    )
    sum7 = (np.mean(term1 / n)) ** 2
    variance = 36 * (sum1 + 2 * sum2 - 2 * sum3 + 4 * sum4 - 2 * sum5 + sum6 - 4 * sum7)
    return max(0, variance)
