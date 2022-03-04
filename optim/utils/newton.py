import numpy as np
from scipy.linalg import lu_solve, lu_factor

# simple implementation for
# solver for system of non-linear equations
# Euler method in particular

def Euler(X_0, F, J, eps=1e-3):
    # X_0 - the initial point
    # F - vector-function of X
    # J - Jacobi matrix for F with respect to X
    # eps - the finishing condition
    class Solution:
        __slots__ = ('error', 'iters', 'x')

        def __init__(self, error, iters, x) -> None:
            self.error = error
            self.iters = iters
            self.x = x

    def step(X):
        # solve the linear problem at each step
        # via LU factorization
        lu, piv = lu_factor(J(X))
        return lu_solve((lu, piv), -F(X))

    X_0 = np.asarray(X_0)
    iters = 0
    X = X_0 + step(X_0)
    delta = X - X_0
    X_i = X_0
    error = F(X)

    while np.linalg.norm(delta) > eps and iters < 1000:
        error = F(X)
        X_i = X
        X = X + step(X)
        delta = X - X_i
        iters += 1

    return Solution(error, iters, X)


def main():

    def F(X):
        U_0, U_2 = X
        F1 = U_2 - 3*U_0 - 4*U_0**2 - U_2**2 + 20
        F2 = 30 - 2*U_2 + 2*U_0 - U_2**2
        return np.array([F1, F2])

    def J(X):
        U_0, U_2 = X
        return np.array([
            [-3 - 8*U_0, 1 - 2*U_2],
            [2, -2 - 2*U_2],
        ])

    X_0 = [3, 3]
    solution = Euler(X_0, F=F, J=J)

    print(solution.x)
    print(solution.error)
    print(solution.iters)
