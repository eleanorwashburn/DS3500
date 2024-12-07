import pandas as pd
import sankey as sk

def main():
    #Making sure updates in sakney.py work
    #bio = pd.read_csv('data/bio.csv')
    #sk.make_sankey(bio, 'cancer', 'gene')

    #Example with new csv using make_sankey
    #brain = pd.read_csv('data/BrainCancer.csv').dropna()
    #sk.make_sankey(brain, 'diagnosis', 'loc')

    #Examle with new csv and aggregation
    bike = pd.read_csv('data/Bikeshare.csv')
    bike_agg = bike.groupby(['mnth', 'weathersit'])['bikers'].sum().reset_index()
    sk.make_sankey(bike_agg, 'mnth', 'weathersit', 'bikers')

if __name__ == '__main__':
    main()