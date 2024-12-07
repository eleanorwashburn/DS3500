import plotly.graph_objects as go

source = [0, 0, 3, 3, 1, 4, 4]
target = [1, 2, 2, 1, 2, 4, 3]
value  = [1, 2, 3, 4, 0.5, 1, 1]
label = ['A', 'B', 'C', 'D', 'E']

link = {'source': source, 'target': target, 'value': value,
        'line': {'color': 'black', 'width': 2}}

node = {'label': label, 'pad': 50, 'thickness': 50,
        'line': {'color': 'black', 'width': 4}}

sk = go.Sankey(link = link, node = node)

fig = go.Figure(sk)
fig.show()