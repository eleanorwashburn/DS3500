"""""
File: sankey.py 
Author: Eleanor Washburn 

Description: A wrapper library or plotly sankey visualizations 
"""""
import pandas as pd
import plotly.graph_objs as go

#gets rid of warning we have been getting
pd.set_option('future.no_silent_downcasting', True)

def code_mapping(df, src, targ):
    """""
    Map labels in src and targ columns to integers
    """""
    #Get the distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    #Create a label --> code mapping
    codes = range(len(labels))
    lc_map = dict(zip(labels, codes))

    #Substitute codes for labels in the DF
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels

#with kwargs we are going to do the padding and the thickness of the nodes
def make_sankey(df, src, targ, vals=None, **kwargs):
    """""
    Create a sankey figure 
    df - raw dataframe 
    src - source node column
    targ - target node column
    vals - link values (thickness)
    """""
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    df, labels = code_mapping(df, src, targ)

    link = {'source': df[src], 'target': df[targ], 'value': values}
    #extracting values for thickness and pad in kwargs arguments here by using .get
    #this gets the value of key and if key doesn't exist set a default value
    thickness = kwargs.get('thickness', 50)
    pad = kwargs.get('pad', 50)
    node = {'label': labels, 'thickness': thickness, 'pad': pad}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()

def main():
    bio = pd.read_csv('bio.csv')
    #thihkness/pad here ends up in the kwargs parameter
    #if you remove thickness and/or pad, will go back to default above, gives user flexibility/customizations
    make_sankey(bio, 'cancer', 'gene', 'evidence', thickness=200, pad=100)

if __name__ == '__main__':
    main()

#HW 2 - extend the sankey functionality to make a multi-layered sankey diagram
#trying to make a 3-leveled sankey diagram
#how we might change make_sankey to support multiple columns --> use args!
#for src and targ add *cols (which is an args) --> def make_sankey(df, src, targ, *cols, vals=None, **kwargs)
#then could choose which columns we want --> could serve as a more flexible way of specifying target
#also make sures there is not the possibility that no or only one columns get passed
#add *cols to parameters in def make-sankey and do a transformation using stacking in this function
#define a second utility method that preforms stacking --> source and target names may change
#if you have 4 columns then you would do a-b, b-c, and c-d
#take pairwise values and stack accordingly

#create pairs from columns A - E --> interview question
#cols = ['A', 'B', 'C', 'D', 'E')
#list(zip(cols, cols[1:]))
#HW2 example
#for src, targ in zip(cols, cols[1:]):
    #print(src, targ)
#zip is a pairwise alignment of the values from 1-2, 2-3 so you do not need to include A in it hence [1:]
