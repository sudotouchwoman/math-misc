from numpy.random import default_rng
from scipy.spatial import distance_matrix

T_START = 1e8
T_END = 1e-4

COOLING_FACTOR = .95
RESTARTS = 1

VERBOSE = True
CITIES = 10
DIMS = 3
SEED = 42

def generate_cities(n=5, dims=2, seed=42):
    rng = default_rng(seed=seed)
    cities_coords = rng.normal(size=(n, dims))
    path_matrix = distance_matrix(cities_coords, cities_coords, p=2)
    return cities_coords, path_matrix


def set_salesman_problem(path_matrix, seed=42):
    rng = default_rng(seed=seed)
    cities = len(path_matrix)

    def cost_function(X):
        cost = .0
        for i, j in zip(X[:-1], X[1:]):
            cost += path_matrix[i, j]
        cost += path_matrix[X[-1], X[0]]
        return cost

    def reverse(X):
      segment = rng.choice(X, size=2, replace=False)
      segment.sort()
      start, end = segment[0], segment[1]

      to_flip = np.arange(start, end)
      X[to_flip] = X[np.flip(to_flip)]
      return X

    def swap(X):
      segment = rng.choice(X, size=2, replace=False)
      segment.sort()
      start, end = segment[0], segment[1]

      X[start], X[end] = X[end], X[start]
      return X

    def permutation_function(X):
      funcs = [reverse, swap]
      return rng.choice(funcs)(X)

    def initial_guess():
        rng = default_rng(seed=seed)
        return rng.permutation(cities)

    return initial_guess, cost_function, permutation_function
