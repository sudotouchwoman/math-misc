import plotly.graph_objects as go
import pandas as pd

# draw the cities as dots in
# euclidean space and connect them
# in accordance with the obtained
# suboptimal solution during simulated
# annealing
def make_path(cities, trace):

    cycle = np.vstack((cities[trace], cities[trace[0]]))
    dims = cities.shape[1]
    layout = {'width': 800, 'height': 800}

    if dims is 3:
      df = pd.DataFrame({
          'X': cycle[:, 0],
          'Y': cycle[:, 1],
          'Z': cycle[:, 2],
      })

      fig = px.line_3d(df, x='X', y='Y', z='Z', markers=True, title=f'TSP Solution on {len(cities)} vertices')

    if dims is 2:
      df = pd.DataFrame({
          'X': cycle[:, 0],
          'Y': cycle[:, 1],
      })

      fig = px.line(df, x='X', y='Y', markers=True, title=f'TSP Solution on {len(cities)} vertices')

    fig.update_layout(layout)
    return fig


# make line plot of the annealing process
# i.e. cost selected during the run
# and minimal (maximal, i.e. optimal) cost
def plot_report(report):
    costs = report['costs']
    cost_opt = report['cost_opt']
    best_costs = report['best_costs']

    df = pd.DataFrame({
        'Cost': costs,
        'Best costs': best_costs
    })

    df.index.names = ['Iteration']
    fig = px.line(df, y=['Cost', 'Best costs'], title=f'Path costs during Annealing. Best: {cost_opt}')
    return fig


# this one is experimental and requires working on
# to understand how buttons and animation work in plotly
def make_animation(cities, traces):

    paths = [
        pd.DataFrame({
        'x': cities[order, 0],
        'y': cities[order, 1],
        'z': cities[order, 2],
        }) for order in traces
    ]

    initial_path, paths = paths[0], paths[1:]

    marker = {'size': 4}
    line = {'color': 'darkblue', 'width': 2}
    updatemenus = [{'type': 'buttons', 'buttons': [{'label': 'Play', 'method': 'animate', 'args': [None]}]}]

    fig = go.Figure(
        data=go.Scatter3d(x=initial_path['x'], y=initial_path['y'], z=initial_path['z'], marker=marker, line=line),
        layout=go.Layout(updatemenus=updatemenus),
        frames=[go.Frame(data=go.Scatter3d(x=path['x'], y=path['y'], z=path['z'], marker=marker, line=line), name=f'It: {i}') for i, path in enumerate(paths)]
    )

    frame_args = {
            "frame": {"duration": 0},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": 0, "easing": "linear"},
        }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    fig.update_layout(title='data HEATPILES', autosize=False, width=650, height=500, margin=dict(l=0, r=0, b=0, t=0))
    fig.update_layout(sliders=sliders)
    return fig
