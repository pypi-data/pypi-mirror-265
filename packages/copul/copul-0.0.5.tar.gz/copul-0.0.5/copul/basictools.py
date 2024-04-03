import numpy as np


def monte_carlo_integral(func, n_samples=10_000, x=1, y=1):
    np.random.seed(1)
    samples_x = np.random.rand(n_samples)
    samples_x = samples_x * x
    samples_y = np.random.rand(n_samples)
    samples_y = samples_y * y
    values = np.mean([func(x, y) for x, y in zip(samples_x, samples_y)])
    return values
