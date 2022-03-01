import plotly.graph_objects as go
from plotly.subplots import make_subplots

def viz_benchmark(policies, average_rewards, optimal_choices_ratio, title=''):

    reward_traces = [
        go.Scatter(
            y=average_rewards[i],
            name=f'{name} Reward',
            mode='markers')
            for i, name in enumerate(policies)]

    reward_traces_cum = [
        go.Scatter(
            y=average_rewards.cumsum(axis=1)[i],
            name=f'{name} Cumulative Reward',
            mode='lines')
            for i, name in enumerate(policies)]

    choice_traces = [
        go.Scatter(
            y=optimal_choices_ratio[i],
            name=f'{name} % Optimal Actions',
            mode='markers')
            for i, name in enumerate(policies)]

    fig = make_subplots(
        rows=1, cols=3, shared_xaxes=True,
        horizontal_spacing=.05,
        subplot_titles=['Average Reward', 'Average Cumulative Reward', '% of Optimal Choices'])

    for trace in reward_traces:
        fig.append_trace(trace, row=1, col=1)

    for trace in reward_traces_cum:
        fig.append_trace(trace, row=1, col=2)

    for trace in choice_traces:
        fig.append_trace(trace, row=1, col=3)

    fig.update_layout(title_text='N-Armed Bandits: Agents Benchmark '+title)
    return fig
