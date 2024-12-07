import plotly.graph_objects as go

source = [0, 0, 0, 1, 1, 2, 2, 2]
target = [3, 4, 5, 3, 5, 3, 4, 5]
value  = [1, 1, 1, 1, 2, 2, 0.5, 1]
label = ['Stomach', 'Lung', 'Brain', 'Gx', 'Gy', 'Gz']

"""""
Mock data table we are pulling from: 
Stomach, Gx, 1
Stomach, Gy, 1
...
Brain, Gz, 1

Purpose of wrapper is to take table and turn into Sankey diagram
with 3-4 inputs. 
"""
link_colors = ['lightgrey'] * 8 #name of color
link_colors[5] = '#F4B212' #rgba hexadecimal
link_colors[3] = 'rgba(145, 154, 232, 0.5)' #rgb and alpha values

node_colors = ['mediumslateblue'] * 3 + ['palegoldenrod'] * 3 #we have 6 nodes
                #disease                    gene

link = {'source': source, 'target': target, 'value': value,
        'line': {'color': 'black', 'width': 2},
        'color': link_colors}

node = {'label': label, 'pad': 50, 'thickness': 50,
        'line': {'color': 'black', 'width': 2},
        'color': node_colors}

sk = go.Sankey(link = link, node = node)

fig = go.Figure(sk)
fig.show()