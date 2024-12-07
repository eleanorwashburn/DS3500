"""
Liam Thompson and Eleanor Washburn
HW 2 - Museum of Contemporary Art
9/25/2024
"""

import plotly.graph_objects as go
import pandas as pd

def aggregate_df(df, group_columns, threshold=None, capitalize_columns=None):
    '''
    Takes in a data frame and aggregates it based on specified column names
    and optional threshold requirements. Capable of capitalizing column names
    to improve downstream functionality if needed. Returns a new data frame fit
    for a standard Sankey diagram.

    df - dataframe
    group_columns - list of column names
    threshold - int
    capitalize_columns - list of column names
    '''
    # Group by the specified columns and count occurrence
    aggregated_df = df.groupby(group_columns).size().reset_index(name='Count')

    # Filter out rows below given count
    aggregated_df = aggregated_df[aggregated_df['Count'] >= threshold]

    # Capitalize specified columns
    if capitalize_columns:
        for col in capitalize_columns:
            if col in aggregated_df.columns:
                aggregated_df[col] = aggregated_df[col].str.capitalize()

    return aggregated_df

def _code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers """

    # Ensure all entries in the source and target columns are strings
    df[src] = df[src].astype(str)
    df[targ] = df[targ].astype(str)

    # Get the source and target labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Create a label->code mapping
    codes = range(len(labels))

    lc_map = dict(zip(labels, codes))

    # Substitute codes for labels in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels

def stacked_sankey_df(df, cols, threshold=None):
    """
    Takes in a dataframe, a list of column names from that dataframe, and
    optionally a threshold value for filtering out certain rows. Returns a
    stacked dataframe composed of three columns: src, targ, and count. This
    dataframe is useful for creating a Sankey diagram.

    df - dataframe
    cols - list of column names
    threshold - int
    """
    temp_df = df[cols].copy()
    # Establish cols in DF
    column_pairs = list(zip(cols[:-1], cols[1:]))

    # Initialize empty list to hold DataFrames
    dataframes = []

    # Loop through pairs of columns to create DataFrames
    for src, targ in column_pairs:
        temp_df = df[[src, targ]].copy()  #
        temp_df.columns = ['src', 'targ']
        dataframes.append(temp_df)

    # Concatenate all DataFrames in the list
    stacked = pd.concat(dataframes, axis=0, ignore_index=True)

    # Group by 'src' and 'targ' and count occurrences
    counted = stacked.groupby(['src', 'targ']).size().reset_index(name='count')

    # Filter out columns that have a count below a certain threshold
    counted = counted[counted['count'] >= threshold]

    return counted

def make_sankey(df, src, targ, vals=None, *cols, **kwargs):
    """
    Create a sankey figure
    df - Dataframe
    src - Source node column name
    targ - Target node column name
    vals - Value (thickness) column name, defaults to None if none provided
    *cols - positional parameters
    **kwargs - named parameters
    """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    df, labels = _code_mapping(df, src, targ)
    link = {'source': df[src], 'target': df[targ], 'value': values}

    thickness = kwargs.get("thickness", 50)
    pad = kwargs.get("pad", 50)
    node = {'label': labels, 'thickness': thickness, 'pad': pad}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()



