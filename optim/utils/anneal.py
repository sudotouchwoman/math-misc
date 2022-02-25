from numpy import exp
from numpy.random import default_rng

def anneal(T_0, T_end, cooling_factor, iters=None, X_0=None, cost_func=None, permut_func=None, restarts=1, seed=42, verbose=False):
    rng = default_rng(seed=seed)

    # check the arguments provided
    if T_0 < T_end: raise ValueError('Invalid temperature bounds')
    if not ( callable(cost_func) and callable(permut_func) ): raise TypeError('Functions provided must be callable')
    if not 0.0 < cooling_factor < 1.0: raise ValueError('Exponential cooling factor must be in (0;1) range')

    # create generator based on args configuration
    if iters and cooling_factor:
      def _make_gen():

        def _gen():
            T = T_0
            for _ in range(iters):
                yield T
                T *= cooling_factor

        return _gen

    if cooling_factor and not iters:
      def _make_gen():

        def _gen():
            T = T_0
            while T > T_end:
                yield T
                T *= cooling_factor

        return _gen

    X_opt = X = X_0
    cost_opt = cost_ = cost_func(X_0)
    traces, costs, best_costs = [X_0], [cost_], [cost_]

    iters_per_T = len(X)

    for i in range(restarts):

      if verbose:
        print(f'[{i}/{restarts}]::[Current Optimal Cost {cost_opt:6f}]')

      Ts = _make_gen()()

      for T in Ts:

        for _ in range(iters_per_T):

            # obtain permutated input vector
            # and compute its cost
            X = permut_func(X)
            cost = cost_func(X)
            diff = cost - cost_

            # this condition lets the algorithm
            # "explore" the domain and not only hill-climb
            # the chance to pick a worse solution decreases as
            # the temperature T decays (according to the decay schedule)
            if diff < 0 or exp(-diff/T) > rng.random(): cost_ = cost

            # save the metrics
            traces.append(X)
            costs.append(cost_)
            best_costs.append(cost_opt)

            # remember the optimal X
            # and corresponding cost
            if cost >= cost_opt: continue
            X_opt = X
            cost_opt = cost

    if verbose:
      print(f'[{restarts}/{restarts}]::[Finished: Optimal Cost {cost_opt:6f}]')

    return {
        'X_opt': X_opt,
        'cost_opt': cost_opt,
        'traces': traces,
        'costs': costs,
        'best_costs': best_costs
        }
