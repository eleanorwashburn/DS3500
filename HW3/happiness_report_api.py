"""
HW 3 - Dashboards
Liam Thompson and Eleanor Washburn
October 15th, 2024
"""
import sqlite3
import pandas as pd

file = "Happiness_Report.csv"

class HappinessAPI:
    def __init__(self, db_file='happiness.db'):
        self.conn = sqlite3.connect(db_file)

    def get_happiness_factors(self, exclude_life_ladder=False):
        """Fetch a list of all happiness factors in the dataset"""
        query = "SELECT * FROM happiness"
        data = pd.read_sql_query(query, self.conn)
        factors = [col for col in data.columns if col not in ['Country name', 'year']]

        if exclude_life_ladder:
            factors.remove('Life Ladder')

        return factors

    def get_countries(self):
        """Fetch a list of all countries in the dataset"""
        query = "SELECT DISTINCT `Country name` FROM happiness"
        countries = pd.read_sql_query(query, self.conn)
        return countries['Country name'].tolist()

    def get_data_by_country(self, country_name):
        """Retrieve all data for a given country"""
        query = f"SELECT * FROM happiness WHERE `Country name` = '{country_name}'"
        data = pd.read_sql_query(query, self.conn)
        return data

# Load CSV into SQLite database
def initialize_database():
    df = pd.read_csv(file)
    conn = sqlite3.connect('happiness.db')
    df.to_sql('happiness', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()