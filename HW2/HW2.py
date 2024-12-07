"""
Liam Thompson and Eleanor Washburn
HW 2 - Museum of Contemporary Art
9/25/2024
"""

import json
import pandas as pd
from SankeyLibrary import aggregate_df
from SankeyLibrary import make_sankey
from SankeyLibrary import stacked_sankey_df

#gets rid of warning we have been getting
pd.set_option('future.no_silent_downcasting', True)

FILE_NAME = "artists.json"

def read_and_load_data(file_name):
    """
    Reads data from a JSON file and loads it in.

    file_name - str
    """
    #Load the data
    with open(file_name, 'r') as f:
        artists_data = json.load(f)

    return artists_data

def convert_to_df(artists_data):
    """
    Converts the JSON data into a pandas DataFrame and filters it to retain
    relevant information about artists' nationality, gender, and birth decade.

    artists_data -  dict
    """
    # Convert JSON data to DataFrame
    artists_df = pd.DataFrame(artists_data)
    # Filter out rows with invalid 'BeginDate'
    artists_df_filtered = artists_df[artists_df['BeginDate'].notna() & (artists_df['BeginDate'] != 0)]

    # Create a new DataFrame with relevant columns
    artists_narrowed_df = artists_df_filtered[['Nationality', 'Gender', 'BeginDate']].copy()

    # Derive the decade from the birth year and ensure 'Decade' is an integer
    artists_narrowed_df['Decade'] = (artists_narrowed_df['BeginDate'] // 10) * 10

    # Drop 'BeginDate' and capitalize 'Gender' and 'Nationality'
    artists_narrowed_df.drop(columns=['BeginDate'], inplace=True)
    artists_narrowed_df['Gender'] = artists_narrowed_df['Gender'].str.capitalize()
    artists_narrowed_df['Nationality'] = artists_narrowed_df['Nationality'].str.capitalize()

    return artists_narrowed_df

def main():
    artists_data = read_and_load_data(FILE_NAME)

    # Call convert_to_DF to get the narrowed DataFrame
    artists_narrowed_df = convert_to_df(artists_data)

    # Now you can aggregate using the narrowed DataFrame
    nationality_decade_df = aggregate_df(artists_narrowed_df, ['Nationality', 'Decade'], threshold=25)

    # Aggregating by 'Gender' and 'Decade'
    gender_decade_df = aggregate_df(artists_narrowed_df, ['Gender', 'Decade'], threshold=25)

    # Aggregating by 'Nationality' and 'Gender', with capitalization
    nationality_gender_df = aggregate_df(artists_narrowed_df, ['Nationality', 'Gender'], threshold=40,
                                         capitalize_columns=['Nationality', 'Gender'])

    # Create Sankey diagrams
    make_sankey(nationality_decade_df, 'Nationality', 'Decade', 'Count')
    make_sankey(nationality_gender_df, 'Nationality', 'Gender', 'Count')
    make_sankey(gender_decade_df, 'Gender', 'Decade', 'Count')

    #Create multi-leveled Sankey diagram
    cols = ['Nationality', 'Gender', 'Decade']
    stacked_df = stacked_sankey_df(artists_narrowed_df, cols, threshold = 50)
    make_sankey(stacked_df, src='src', targ='targ', vals='count')


if __name__ == '__main__':
    main()