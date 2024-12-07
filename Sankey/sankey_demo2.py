import plotly.graph_objects as go

source = [0, 0, 3, 3, 0, 0]
target = [1, 2, 2, 1, 3, 0]
value  = [1, 2, 3, 4, 1, 1]

label = ['A', 'B', 'C', 'D']

link = {'source': source, 'target': target, 'value': value}
node = {'label': label, 'pad': 50, 'thickness': 50}

sk = go.Sankey(link = link, node = node)

fig = go.Figure(sk)
fig.show()

