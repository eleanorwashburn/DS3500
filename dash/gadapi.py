"""
File: gadapi.py

Description: The primary api for interacting with the gad dataset
"""
import pandas as pd
import sankey as sk
from collections import Counter

class GADAPI:

    # This will be a dataframe and it is none to indicate it is an internal state object
    gad = None

    def load_gad(self, filename):
        self.gad = pd.read_csv(filename)
        # NEED TO CLEAN
        # one row is one publication so disease name can be mentioned many times
        # Sometimes the one row lists multiple disease by commas or semicolons
        # inconsistencies DF from naming conventions with disease names
        print(self.gad)

    def get_phenotypes(self):
        """Fetch the list of unique phenotypes (diseases) with at least
        one positive association in the GAD dataset"""
        gady = self.gad[self.gad.association == 'Y']
        # Making all phenotypes to lowercase
        gady.phenotype = gady.phenotype.str.lower()
        phen = gady['phenotype'].unique()
        # This is us cleaning a bit
        # Turned p into strings to can be iterable (got an error previously without it)
        phen = [str(p) for p in phen if ';' not in str(p)]
        return sorted(phen)

    # Local network is starting with a specific disease and finding the genes associated with it
    # (not showing all the combos of genes and disease)
    # min_pub is to help filter the data (only showing the highly confirmed connections) to render insightful plots
    def extract_local_network(self, phenotype, min_pub, singular):
        # Positive associations only!
        gad = self.gad[self.gad.association == 'Y']

        # Focus on a particular set of columns
        gad = gad[['phenotype', 'gene']]

        # Convert the phenotype to lowercase --> should be predefined DF in object so its stored and not repeated
        gad.phenotype = gad.phenotype.str.lower()

        # Count publications (rows) for each unique disease-gene association
        gad = gad.groupby(['phenotype', 'gene']).size().reset_index(name='npubs')

        # Sort by npubs descending
        gad.sort_values('npubs', ascending=False, inplace=True)

        # Discard associations with less than <min_pub> publications
        gad = gad[gad.npubs >= min_pub]

        # Phenotype of interest
        gad_pheno = gad[gad.phenotype == phenotype]

        # Find all gad associations involving genes linked to our starting phenotype
        gad = gad[gad.gene.isin(gad_pheno.gene)]

        # Discard singular disease-gene associations
        if not singular:
            counts = Counter(gad.phenotype)
            exclude = [k for k, v in counts.items() if v == 1]
            gad = gad[~gad.phenotype.isin(exclude)] # ~ means finds the rows that are in exclusion list and negate them

        return gad

def main():
    gadapi = GADAPI()
    gadapi.load_gad('gad.csv')

    phen = gadapi.get_phenotypes()
    for p in phen:
        print(p)

    print(len(phen))

    local = gadapi.extract_local_network('asthma', )
    print(local)
if __name__ == "__main__":
    main()