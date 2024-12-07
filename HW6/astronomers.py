from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import string
import matplotlib.pyplot as plt
import math
import numpy as np

def create_timeline(data, title="Timeline", filename=None):
    """
    Creates a timeline visualization of astronomer works with different colors for each work.

    Parameters:
    - data: List of tuples in the format (label, year, description)
    - title: Title of the timeline
    - filename: If provided, saves the timeline as a file (e.g., 'timeline.png')
    """
    # Extract years, labels, and descriptions
    years = [entry[1] for entry in data]

    # Create a color map with distinct colors for each work
    colors = plt.cm.get_cmap('tab10', len(data))  # Using 'tab10' colormap for distinct colors

    # Create the figure
    plt.figure(figsize=(15, 9))

    # Plot points for each year with different colors and store legend labels
    legend_labels = []
    for i, (label, year, description) in enumerate(data):
        plt.scatter(year, 1, color=colors(i), s=100)  # Scatter with unique color for each point
        legend_labels.append(f"{label} ({year}): {description}")  # Add label with work name to legend

    # Add aesthetics
    plt.axhline(y=1, color='gray', linestyle='--', linewidth=0.7)
    plt.yticks([])# Remove y-axis ticks
    plt.xticks(sorted(years), fontsize=12, rotation=45)  # Ensure sorted years
    plt.xlabel("Year", fontsize=12)
    plt.title(title, fontsize=16)

    # Adjust x-axis limits to add more space (set padding around the min and max years)
    plt.xlim(min(years) - 5, max(years) + 5)  # Adding space before the first year and after the last year

    # Create a legend based on the colors
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors(i), markersize=10) for i in
               range(len(data))]
    # Move the legend below and make it horizontal
    plt.legend(handles, legend_labels, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=3, fontsize=10)

    plt.tight_layout()

    # Show or save the plot
    plt.show()

class AstroTextLibrary:
    def __init__(self):
        self.data = {}
        self.max_files = 10
        self.stop_words = set()
        self.parts_of_speech = set()
        self.allowed_two_letter_words = {"in", "on", "at", "by", "an", "it", "is", "as"}

    def load_text(self, filename, label, parser=None):
        """
        Loads and processes a text file. Allows for a customer parser to be called.
        """
        if len(self.data) >= self.max_files:
            raise Exception("Maximum of 10 files can be loaded.")

        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        processed_data = parser(text) if parser else self._default_parser(text)
        self.data[label] = processed_data
        print(f"Loaded file '{filename}' with label '{label}'.")

    def load_stop_words(self, stopfile):
        """
        Loads a list of stop words.
        """
        with open(stopfile, 'r', encoding='utf-8') as f:
            stop_words = {line.strip() for line in f if line.strip()}
            self.stop_words = stop_words
            print(f"Loaded {len(self.stop_words)} stop words from '{stopfile}'.")

    def load_parts_of_speech(self, speech_file):
        """
        Loads a list of parts of speech words.
        """
        with open(speech_file, 'r', encoding='utf-8') as f:
            parts_of_speech = {line.strip() for line in f if line.strip()}
            self.parts_of_speech = parts_of_speech
            print(f"Loaded {len(self.parts_of_speech)} stop words from '{speech_file}'.")

    def _default_parser(self, text):
        """
        A generic parser meant to eliminate trivial words that will not contribute to
        valuable text analysis. Useful in any domain.
        """
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = text.split()

        filtered_words = [
            word for word in words
            if word.isalpha() and word not in self.stop_words and
               (len(word) > 2 or word in self.allowed_two_letter_words)]

        word_count = Counter(filtered_words)
        word_length = Counter(len(word) for word in filtered_words)

        return {
            'clean_text': clean_text,
            'wordcount': word_count,
            'word_length': word_length,
            'numwords': len(filtered_words),
        }

    def astronomy_parser(self, text):
        """
        This is a custom parser built for astronomers' documents. Attempts to hone in
        on terms used in such works.
        """
        common_astronomy_terms = {
            "moon", "sun", "earth", "star", "nova", "orbit", "venus", "mars",
            "space", "light", "time", "pluto", "comet", "sirius", "galax", "vesta",
            "lunar", "solar", "altair", "quark", "aries", "terra", "black", "atoms", "quasi",
            "belt", "rock"
        }

        clean_text = text.replace('\n', ' ').lower()
        words = text.split()

        filtered_words = [
            word for word in words
            if word.isalpha() and word not in self.stop_words and
               (len(word) > 5 or word in common_astronomy_terms)
        ]
        word_count = Counter(filtered_words)
        word_length = Counter(len(word) for word in filtered_words)

        common_astronomy_terms_counts = {}
        for word in common_astronomy_terms:
            if word in word_count:
                common_astronomy_terms_counts[word] = word_count[word]

        return {
            'clean_text': clean_text,
            'wordcount': word_count,
            'word_length': word_length,
            'numwords': len(filtered_words),
            'common_astronomy_terms_counts': common_astronomy_terms_counts,
        }

    def compare_num_words(self):
        """
        Prints the word count for each given text.
        """
        comparison = {label: data['numwords'] for label, data in self.data.items()}
        print("Word Count Comparison:")
        for label, count in comparison.items():
            print(f"{label}: {count} words")

    def print_top_words(self, top_n=25):
        """
        Prints the top 25 most used words in each text.
        """
        for label, data in self.data.items():
            print(f"\nTop {top_n} Words in '{label}':")
            top_words = data['wordcount'].most_common(top_n)
            for word, count in top_words:
                print(f"{word}: {count}")

    def create_timeline(data, title="Timeline", filename=None):
        """
        Creates a timeline visualization.

        Parameters:
        - data: List of tuples in the format (label, year, description)
        - title: Title of the timeline
        - filename: If provided, saves the timeline as a file (e.g., 'timeline.png')
        """
        # Extract years, labels, and descriptions
        years = [entry[1] for entry in data]
        labels = [f"{entry[0]} ({entry[1]})\n{entry[2]}" for entry in data]

        # Alternate y-positions to avoid overlapping
        y_positions = [1.2 if i % 2 == 0 else 0.8 for i in range(len(years))]

        # Create the figure
        plt.figure(figsize=(12, 6))

        # Plot points for each year
        plt.scatter(years, [1] * len(years), color="blue", s=100, label="Works")

        # Add labels at alternating heights
        for year, label, y_pos in zip(years, labels, y_positions):
            plt.text(year, y_pos, label, rotation=30, ha="right", fontsize=10)

        # Add aesthetics
        plt.axhline(y=1, color='gray', linestyle='--', linewidth=0.7)
        plt.yticks([])  # Remove y-axis ticks
        plt.xticks(sorted(years), fontsize=12, rotation=45)  # Ensure sorted years
        plt.xlabel("Year", fontsize=12)
        plt.title(title, fontsize=16)
        plt.tight_layout()
        plt.show()

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generate a Sankey diagram mapping each text to words, where the thickness represents
        word counts. The world_list is a list of user-specified words. If not provided, the
        Sankey diagram will use a default k-value of 5 to get the most common words
        (as a union across all texts) to include.
        """
        if not word_list:
            top_k_words_union = set()
            for data in self.data.values():
                top_k_words = [word for word, _ in data['wordcount'].most_common(k)]
                top_k_words_union.update(top_k_words)
            word_list = top_k_words_union

        sankey_data = []

        for label, data in self.data.items():
            filtered_words = {word: count for word, count in data['wordcount'].items() if word in word_list}
            for word, count in filtered_words.items():
                sankey_data.append({"source": label, "target": word, "value": count})

        sankey_df = pd.DataFrame(sankey_data)

        self._make_sankey(sankey_df, src="source", targ="target", vals="value",
                          pad=50, thickness=30)

    def _make_sankey(self, df, src, targ, vals, **kwargs):
        """
        Helper function to generate a Sankey diagram.
        """
        labels = sorted(set(df[src]).union(set(df[targ])))
        label_map = {label: i for i, label in enumerate(labels)}

        df[src] = df[src].map(label_map)
        df[targ] = df[targ].map(label_map)

        link = {
            "source": df[src],
            "target": df[targ],
            "value": df[vals]
        }

        node = {
            "label": labels,
            "pad": kwargs.get("pad", 50),
            "thickness": kwargs.get("thickness", 30),
            "line": {
                "color": kwargs.get("line_color", "black"),
                "width": kwargs.get("line_width", 1),
            },
        }

        fig = go.Figure(go.Sankey(link=link, node=node))
        fig.update_layout(
            title_text="Word Count Sankey Diagram",
            font_size=10,
            width=kwargs.get("width", 1000),
            height=kwargs.get("height", 600),
        )
        fig.show()

    def visualize_concept_focus(self, layout=None):
        """
        Create a subplot visualization of pie charts showing observational vs. theoretical keyword focus
        for each text file.
        """
        observation_keywords = {
            "telescope", "star", "planet", "moon", "galaxy", "nebula",
            "constellation", "comet", "asteroid", "satellite", "eclipse",
            "orbit", "spectrum", "light", "sun", "mars", "jupiter",
            "venus", "mercury", "saturn", "uranus", "neptune", "pluto",
            "meteor", "aurora", "crater", "phases", "rings", "pulsar",
            "supernova"
        }

        theory_keywords = {
            "time", "gravity", "black hole", "relativity", "quantum", "matter",
            "energy", "universe", "spacetime", "singularity", "expansion",
            "cosmology", "inertia", "curvature", "force", "dark matter",
            "antimatter", "entropy", "dimension", "big bang", "multiverse",
            "equation", "fields", "mass", "light speed", "strings"
        }

        num_texts = len(self.data)
        if num_texts < 2 or num_texts > 10:
            raise ValueError("Number of texts must be between 2 and 10.")

        if not layout:
            cols = math.ceil(math.sqrt(num_texts))
            rows = math.ceil(num_texts / cols)
        else:
            rows, cols = layout

        fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
        axes = axes.flatten()

        i = -1
        for i, (label, data) in enumerate(self.data.items()):
            ax = axes[i]

            word_count = data["wordcount"]
            observation_count = sum(word_count.get(keyword, 0) for keyword in observation_keywords)
            theory_count = sum(word_count.get(keyword, 0) for keyword in theory_keywords)

            total = observation_count + theory_count
            if total == 0:
                ax.text(0.5, 0.5, "No Relevant Keywords", ha="center", va="center", fontsize=12)
                ax.axis("off")
                continue

            labels = ["Observation", "Theory"]
            values = [observation_count, theory_count]
            colors = ["skyblue", "lightcoral"]
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
            ax.set_title(label, fontsize=13, fontweight="bold")

        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        fig.tight_layout()
        plt.show()

    def get_top_words_per_document(self, n=3):
        """
        Get the top N words for each document and their frequencies, normalized by document length.
        Returns a DataFrame where columns are ['Document', 'Word', 'Frequency'].
        """
        data = []

        # Loop through each document
        for label, doc_data in self.data.items():
            total_words = doc_data['numwords']  # Total number of words in the document
            top_words = doc_data['wordcount'].most_common(n)

            # Normalize word frequency by the total number of words in the document
            for word, freq in top_words:
                normalized_freq = freq / total_words  # Normalize frequency
                data.append({'Document': label, 'Word': word, 'Frequency': normalized_freq})

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df

    def plot_top_words_bar_chart(self, df):
        """
        Plot a bar chart showing the top N words for each document, with each word having its own color.
        Frequencies are normalized by document length to account for varying document sizes.
        """

        def extract_year(doc_label):
            if doc_label[-6] == '(' and doc_label[-1] == ')':
                year_str = doc_label[-5:-1]  # Extract characters between '(' and ')'
                if year_str.isdigit():
                    return int(year_str)  # Convert to int, default to 0 if not valid

        # Add a 'Year' column to help with sorting
        df['Extracted Year'] = df['Document'].apply(extract_year)

        # Sort the DataFrame by the 'Extracted Year' column (chronologically)
        df = df.sort_values('Extracted Year')

        # Pivot the data for plotting
        pivot_df = df.pivot(index='Document', columns='Word', values='Frequency').fillna(0)

        # Sort the pivot DataFrame to ensure the order is by 'Document' as well
        pivot_df = pivot_df.loc[df['Document'].unique()]  # Sort according to the order of documents

        # Generate a consistent color palette for the unique words
        unique_words = pivot_df.columns
        color_palette = plt.cm.tab20.colors  # Use a colormap with enough distinct colors
        word_colors = {word: color_palette[i % len(color_palette)] for i, word in enumerate(unique_words)}

        # Map word colors to the columns of the DataFrame
        bar_colors = [word_colors[word] for word in pivot_df.columns]

        # Plot the bar chart
        ax = pivot_df.plot(
            kind='bar',
            stacked=True,
            figsize=(12, 8),
            color=bar_colors,
        )

        # Explicitly set the order of x-ticks to match the chronological order
        ax.set_xticklabels(pivot_df.index, rotation=45)

        # Add titles and labels
        plt.title("Top Words for Each Document (Chronological Order)", fontsize=16)
        plt.xlabel("Documents", fontsize=12)
        plt.ylabel("Word Frequency", fontsize=12)
        plt.legend(
            title="Words",
            labels=pivot_df.columns,
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
        )
        plt.tight_layout()
        plt.show()

def main():
    astronomer_works = [
        ("Copernicus", 1514, "Commentariolus"),
        ("Copernicus", 1543, "On the Revolutions of the Heavenly Spheres"),
        ("Galileo", 1610, "Sidereus Nuncius"),
        ("Bradley", 1727, "Motion of Fixed Stars"),
        ("Herschel", 1849, "Outlines of Astronomy"),
        ("Hubble", 1923, "The Faint Nebulae"),
        ("Hubble", 1936, "The Realm of the Nebulae"),
        ("Sagan", 1980, "Cosmos"),
        ("Hawking", 1988, "A Brief History of Time"),
        ("Hawking", 2005, "The Great Collider"),
    ]

    create_timeline(data=astronomer_works, title="Timeline of Major Astronomical Works")

    # Create instance of the AstroTextLibrary
    star = AstroTextLibrary()

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

    # Display loaded data
    star.compare_num_words()

    # Print top 25 words from each file
    star.print_top_words(top_n=25)

    # Generate Sankey diagram for the top 5 words (default)
    star.wordcount_sankey()

    # Generate Sankey diagram for a custom word list
    star.wordcount_sankey(word_list=["star", "galaxy", "future"])

    # Visualize sentiment scores with default layout
    star.visualize_concept_focus()

    # Get top 3 words for each document
    top_words_df = star.get_top_words_per_document(n=3)

    # Plot a bar chart for the top words
    star.plot_top_words_bar_chart(top_words_df)

if __name__ == '__main__':
    main()