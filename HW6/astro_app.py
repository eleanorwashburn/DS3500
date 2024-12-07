"""
astro_app.py
Eleanor Washburn and Liam Thompson
"""

from astro_text_library import AstroTextLibrary

def main():
    # Create instance of the AstroTextLibrary
    star = AstroTextLibrary()

    # Create a timeline of major astronomical works with a specified title
    star.create_timeline(title="Timeline of Major Astronomical Works")

    # Load custom stop words from a file
    star.load_stop_words('ranks_nl_stopwords.txt')

    # Load text files in chronological order; text publication dates featured in order
    star.load_text('Copernicus_Commentariolus.txt', 'Copernicus (1514)', parser=star.astronomy_parser)
    star.load_text('Copernicus_HeavenlySpheres.txt', 'Copernicus (1543)', parser=star.astronomy_parser)
    star.load_text('Galileo_SidereusNuncius.txt', 'Galileo (1610)', parser=star.astronomy_parser)
    star.load_text('Bradley_MotionOfFixedStars.txt', 'Bradley (1727)', parser=star.astronomy_parser)
    star.load_text('Herschel_OutlinesOfAstronomy.txt', 'Herschel (1849)', parser=star.astronomy_parser)
    star.load_text('Hubble_FaintNebulae.txt', 'Hubble (1923)', parser=star.astronomy_parser)
    star.load_text('Hubble_RealmOfNebulae.txt', 'Hubble (1936)', parser=star.astronomy_parser)
    star.load_text('Sagan_Cosmos.txt', 'Sagan (1980)', parser=star.astronomy_parser)
    star.load_text('Hawking_BriefHistoryOfTime.txt', 'Hawking (1988)', parser=star.astronomy_parser)
    star.load_text('Hawking_GreatCollider.txt', 'Hawking (2005)', parser=star.astronomy_parser)

    # Generate a Sankey diagram for the 3 most common words across each text file
    star.wordcount_sankey(k=3)

    # Generate a Sankey diagram for a custom word list (e.g., "star", "galaxy", "future")
    star.wordcount_sankey(word_list=["earth", "sun", "star", "galaxy", "universe"])

    # Visualize the conceptual focus (observation vs. theory) of each text using pie charts
    star.conceptual_pies()

    # Display a bar chart with the top 3 most common words in each text file
    star.top_words_bars(n=3)

if __name__ == '__main__':
    main()