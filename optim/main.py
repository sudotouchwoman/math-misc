from utils.salesman import *
from utils.anneal import anneal
from utils.viz import make_path, plot_report

def main():
    cities, paths = generate_cities(CITIES, dims=DIMS, seed=SEED)
    initial_guess, cost_function, permutation_function = set_salesman_problem(paths)

    X_0 = initial_guess()
    report = anneal(
        T_START,
        T_END,
        COOLING_FACTOR,
        X_0=X_0,
        cost_func=cost_function,
        permut_func=permutation_function,
        restarts=RESTARTS,
        verbose=VERBOSE
        )

    make_path(cities, trace=report['X_opt'])
    plot_report(report).show()

if __name__ == '__main__':
    main()
