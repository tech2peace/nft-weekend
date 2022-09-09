import numpy as np
from scipy import stats as stats


def sample_centers(forms_count, l_count, dist, R=1, r=0.1):
    dim = int(forms_count / 2)
    lower, upper = -R + r, R - r
    if dist == "normal":
        mu, sigma = 0, 0.7
        X = stats.truncnorm(
            (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        C = X.rvs(size=(l_count, dim))
    elif dist == "uniform":
        C = np.random.uniform(lower, upper, size=(l_count, dim))
    return C