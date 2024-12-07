import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('bio_encoded.csv')
print(df)

#Will not work, but it showcases what we are trying to do
#Now does work because we changed data to actual data --> bio.csv to bio_encoded.csv
#This is because strings now are #s --> wrapper functionality is doing this then to diagram

link = {'source': df.source, 'target': df.target, 'value': df.value,
        'line': {'color': 'black', 'width': 2}}

node = {'label': ['?'] * 6, 'pad': 50, 'thickness': 50,
        'line': {'color': 'black', 'width': 2}}

sk = go.Sankey(link=link, node=node)
fig = go.Figure(sk)
fig.show()

