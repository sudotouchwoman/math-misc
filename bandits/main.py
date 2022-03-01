from utils.policies import benchmark_template
from utils.viz import viz_benchmark
from utils import N_ARMS, N_BANDITS, ITERS

def main():
    average_rewards, optimal_choices, policies_names = benchmark_template(N_ARMS, N_BANDITS, ITERS)
    fig = viz_benchmark(
        policies_names,
        average_rewards,
        optimal_choices,
        title=f'({N_ARMS} Arms, {N_BANDITS} Bandits)')
    fig.show()


if __name__ == '__main__':
    main()
