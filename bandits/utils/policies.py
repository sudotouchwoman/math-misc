import numpy as np
from numpy.random import default_rng

def make_bandits(n_arms, n_bandits, seed=42):
    gen = default_rng(seed=seed)
    mean, std = .0, 1.
    return gen.normal(mean, std, size=(n_bandits, n_arms))


class EpsGreedy:

    def __init__(self, eps, n, seed=42):
        self.gen = default_rng(seed=seed)
        self.eps = eps
        self.q = np.zeros(n)
        self.picks = np.zeros(n)
        self.rewards = np.zeros(n)


    def __call__(self, X):
        current_best = self.q.argmax()
        mask = X == X
        mask[current_best] = False

        if self.gen.random() < self.eps: choice = self.gen.choice(X[mask])
        else: choice = X[self.q.argmax()]

        mean, std = .0, .1
        noised = lambda x: x + self.gen.normal(mean, std)

        mask = X == choice
        self.picks[mask] += 1
        self.rewards[mask] += noised(choice)
        self.q[mask] = self.rewards[mask] / self.picks[mask]    
        return choice


class UCB:
    # Upper Confidence Bound learner
    def __init__(self, c, n, seed=42):
        self.gen = default_rng(seed=seed)
        self.c = c  # the exploration rate
        self.q = np.zeros(n)
        self.picks = np.zeros(n)
        self.rewards = np.zeros(n)
        self.t = 0


    def __call__(self, X):
        # the main property of this agent
        # is its ability to choose among non-greedy actions
        # by a root term, representing variance in the estimate
        # of the given action (this decays through time and picks)
        yet_unplayed = self.picks == np.zeros_like(self.picks)
        if yet_unplayed.any():
            choice = self.gen.choice(X[yet_unplayed])
            mask = X == choice
        else:
            UCB = self.q + self.c * np.sqrt(np.log(self.t) / self.picks)
            choice = UCB.max()
            mask = choice == UCB

        mean, std = .0, .1
        noised = lambda x: x + self.gen.normal(mean, std)

        self.picks[mask] += 1
        self.rewards[mask] += noised(choice)
        self.q[mask] = self.rewards[mask] / self.picks[mask]
        self.t += 1
        return X[mask]


def policy_template(agent, **kwargs):
    # helper function to wrap policy (agent)
    # and create an instance on call
    if agent.lower() == 'eps':
        return lambda: EpsGreedy(**kwargs)
    if agent.lower() == 'ucb':
        return lambda: UCB(**kwargs)


def benchmark_policies(policies, bandits, iters=1000, seed=100):
    average_rewards = np.zeros((len(policies), iters))
    optimal_choices = np.zeros_like(average_rewards)

    for bandit in bandits:
      best_action = bandit.max()

      for p, policy in enumerate(policies):
        policy = policy()

        for i in range(iters):
              score = policy(bandit)
              average_rewards[p, i] += score
              optimal_choices[p, i] += best_action == score

    return average_rewards / len(bandits), optimal_choices / len(bandits)


def benchmark_template(arms, bandits, iters, epsilon_grid=None, c_grid=None):
    # create grids for parameters if ones not provided
    if epsilon_grid is None: epsilon_grid = np.geomspace(1e-3, 1e-1, 3)
    if c_grid is None: c_grid = np.geomspace(1e-4, 1e-2, 2)

    # create set of configs for agents
    eps_kwargs = [{'n': arms, 'eps': eps, 'seed': seed} for seed, eps in enumerate(epsilon_grid)]
    ucb_kwargs = [{'c': c, 'n': arms, 'seed': seed} for seed, c in enumerate(c_grid)]
    
    # create policy blueprints and their titles
    policies = [policy_template('eps', eps=.0, n=arms)] + [policy_template('eps', **kwargs) for kwargs in eps_kwargs] + [policy_template('UCB', **kwargs) for kwargs in ucb_kwargs]
    policies_names = ['Greedy'] + [f'EPS={eps:.3f} Greedy' for eps in epsilon_grid] + [f'C={c:.4f} UCB' for c in c_grid]
    # the required configuration of bandits
    bandits = make_bandits(n_arms=arms, n_bandits=bandits)
    # it is convenient to be explicit about return types
    average_rewards, optimal_choices = benchmark_policies(policies, bandits, iters=iters)
    return average_rewards, optimal_choices, policies_names
