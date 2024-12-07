"""
astro_text_library.py
Eleanor Washburn and Liam Thompson
"""

from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import string
import matplotlib.pyplot as plt
import math

class AstroTextLibrary:
    def __init__(self):
        """
        Initializes the AstroTextLibrary class.Prepares the data structure
        to store text and associated information.
        """
        # Holds the processed text data
        self.data = {}
        # Limits the number of files that can be loaded
        self.max_files = 10
        # Set for storing stop words
        self.stop_words = set()
        # Allowed short words for analysis
        self.allowed_two_letter_words = {"in", "on", "at", "by", "an", "it", "is", "as"}

    def load_text(self, filename, label, parser=None):
        """
        Loads and processes a text file. Requires a label to be assigned to each file,
        including its publication year in parentheses (e.g., "Text (2002)").
        Also allows for a custom, domain-specific parser to be used.
        """
        # Ensure no more than 10 files are loaded
        if len(self.data) >= self.max_files:
            raise Exception("Maximum of 10 files can be loaded.")

        with open(filename, 'r', encoding='utf-8') as f:
            # Read the content of the text file
            text = f.read()

        # Apply a custom parser if provided, otherwise use the default parser
        processed_data = parser(text) if parser else self._default_parser(text)
        self.data[label] = processed_data
        print(f"Loaded file '{filename}' with label '{label}'.")

    def load_stop_words(self, stopfile):
        """
        Loads a list of stop words from a file to exclude from the analysis.
        """
        with open(stopfile, 'r', encoding='utf-8') as f:
            # Create a set of stop words
            self.stop_word = {line.strip() for line in f if line.strip()}
            print(f"Loaded {len(self.stop_words)} stop words from '{stopfile}'.")

    def _default_parser(self, text):
        """
        A generic parser meant to eliminate trivial words that will not contribute to
        valuable text analysis. Useful in any domain.
        """
        # Remove punctuation and convert to lowercase
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        # Split the text into individual words
        words = text.split()

        # Filter out stop words and non-alphabetic words, and allow short words if they're in the allowed list
        filtered_words = [
            word for word in words
            if word.isalpha() and word not in self.stop_words and
               (len(word) > 2 or word in self.allowed_two_letter_words)]

        # Count occurrences of filtered words and the lengths of the words
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
        # Define a set of common astronomy terms
        common_astronomy_terms = {
            "moon", "sun", "earth", "star", "nova", "orbit", "venus", "mars",
            "space", "light", "time", "pluto", "comet", "sirius", "galax", "vesta",
            "lunar", "solar", "altair", "quark", "aries", "terra", "black", "atoms", "quasi",
            "belt", "rock"}

        # Clean up the text
        clean_text = text.replace('\n', ' ').lower()
        # Split text into words
        words = text.split()

        # Filter words based on length, stop words, and astronomy-related terms
        filtered_words = [
            word for word in words
            if word.isalpha() and word not in self.stop_words and
               (len(word) > 5 or word in common_astronomy_terms)]

        # Count the filtered words
        word_count = Counter(filtered_words)
        # Count word lengths
        word_length = Counter(len(word) for word in filtered_words)

        # Count occurrences of common astronomy terms
        common_astronomy_terms_counts = {}
        for word in common_astronomy_terms:
            if word in word_count:
                common_astronomy_terms_counts[word] = word_count[word]

        return {
            'clean_text': clean_text,
            'wordcount': word_count,
            'word_length': word_length,
            'numwords': len(filtered_words),
            'common_astronomy_terms_counts': common_astronomy_terms_counts,}

    def compare_num_words(self):
        """
        Prints the word count for each given text.
        """
        # Create a dictionary of word counts
        comparison = {label: data['numwords'] for label, data in self.data.items()}
        print("Word Count Comparison:")
        # Print word counts for each label
        for label, count in comparison.items():
            print(f"{label}: {count} words")

    def print_top_words(self, top_n=25):
        """
        Prints the top N most used words in each text.
        """
        for label, data in self.data.items():
            print(f"\nTop {top_n} Words in '{label}':")
            # Get the most common words
            top_words = data['wordcount'].most_common(top_n)
            # Print each word with its count
            for word, count in top_words:
                print(f"{word}: {count}")

    def create_timeline(self, title="Timeline"):
        """
        Creates a timeline visualization of astronomer works with different colors for each work.
        """
        # Data representing the works of various astronomers
        data = [
            ("Copernicus", 1514, "Commentariolus"),
            ("Copernicus", 1543, "On the Revolutions of the Heavenly Spheres"),
            ("Galileo", 1610, "Sidereus Nuncius"),
            ("Bradley", 1727, "Motion of Fixed Stars"),
            ("Herschel", 1849, "Outlines of Astronomy"),
            ("Hubble", 1923, "The Faint Nebulae"),
            ("Hubble", 1936, "The Realm of the Nebulae"),
            ("Sagan", 1980, "Cosmos"),
            ("Hawking", 1988, "A Brief History of Time"),
            ("Hawking", 2005, "The Great Collider"),]

        # Extract years from the data
        years = [entry[1] for entry in data]

        # Create a color map with distinct colors for each work
        colors = plt.cm.get_cmap('tab10', len(data))

        # Create the figure for the timeline
        plt.figure(figsize=(15, 9))
        legend_labels = []

        for i, (label, year, description) in enumerate(data):
            # Plot a point for each work
            plt.scatter(year, 1, color=colors(i), s=100)
            # Add legend label
            legend_labels.append(f"{label} ({year}): {description}")

        # Add a horizontal line for reference
        plt.axhline(y=1, color='gray', linestyle='--', linewidth=0.7)
        # Remove y-axis ticks
        plt.yticks([])
        # Set x-axis ticks
        plt.xticks(sorted(years), fontsize=12, rotation=45)
        plt.xlabel("Year", fontsize=12)
        plt.title(title, fontsize=16)

        # Create legend entries
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors(i), markersize=10) for i in
                   range(len(data))]
        plt.legend(handles, legend_labels, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=3, fontsize=10)

        plt.tight_layout()
        plt.show()

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generate a Sankey diagram mapping each text to words, where the thickness represents
        word counts. The world_list is a list of user-specified words. If not provided, the
        Sankey diagram will use a default k-value of 5 to get the most common words
        (as a union across all texts) to include.
        """
        # If no word list is provided, use the most common words
        if not word_list:
            top_k_words_union = set()
            for data in self.data.values():
                # Get top k words from each text
                top_k_words = [word for word, _ in data['wordcount'].most_common(k)]
                # Merge into one set of top words
                top_k_words_union.update(top_k_words)
            word_list = top_k_words_union

        # List to store Sankey diagram data
        sankey_data = []

        for label, data in self.data.items():
            # Filter words that are in the user-specified list and prepare Sankey data
            filtered_words = {word: count for word, count in data['wordcount'].items() if word in word_list}
            for word, count in filtered_words.items():
                sankey_data.append({"source": label, "target": word, "value": count})

        # Convert the list of Sankey data into a DataFrame
        sankey_df = pd.DataFrame(sankey_data)
        # Call the _make_sankey function to generate the Sankey diagram
        self._make_sankey(sankey_df, src="source", targ="target", vals="value",
                          pad=50, thickness=30)

    def _make_sankey(self, df, src, targ, vals, **kwargs):
        """
        Helper function to generate a Sankey diagram.
        """
        # Create a set of unique labels by combining both source and target values
        labels = sorted(set(df[src]).union(set(df[targ])))
        # Create a mapping from labels to their indices
        label_map = {label: i for i, label in enumerate(labels)}

        # Map the source and target columns to their respective indices based on the label map
        df[src] = df[src].map(label_map)
        df[targ] = df[targ].map(label_map)

        # Prepare the link data for the Sankey diagram: source, target, and value
        link = {
            "source": df[src],
            "target": df[targ],
            "value": df[vals]}
        # Prepare the node data for the Sankey diagram: label and style options (pad, thickness, line)
        node = {
            "label": labels,
            "pad": kwargs.get("pad", 50),
            "thickness": kwargs.get("thickness", 30),
            "line": {
                "color": kwargs.get("line_color", "black"),
                "width": kwargs.get("line_width", 1),},}

        # Create the Sankey figure using Plotly's Sankey chart
        fig = go.Figure(go.Sankey(link=link, node=node))
        # Update the layout of the Sankey diagram (title, font size, dimensions)
        fig.update_layout(
            title_text="Word Count Sankey Diagram",
            font_size=10,
            width=kwargs.get("width", 1000),
            height=kwargs.get("height", 600),)

        # Show the Sankey diagram
        fig.show()

    def conceptual_pies(self):
        """
        Create a subplot visualization of pie charts showing the observational vs. theoretical keyword focus
        for each text file. Automatically arranges pie charts in a grid layout.
        """
        # Define sets of observation-related keywords
        observation_keywords = {
            "telescope", "star", "planet", "moon", "galaxy", "nebula",
            "constellation", "comet", "asteroid", "satellite", "eclipse",
            "orbit", "spectrum", "light", "sun", "mars", "jupiter",
            "venus", "mercury", "saturn", "uranus", "neptune", "pluto",
            "meteor", "aurora", "crater", "phases", "rings", "pulsar",
            "supernova"
        }

        # Define sets of theory-related keywords
        theory_keywords = {
            "time", "gravity", "black hole", "relativity", "quantum", "matter",
            "energy", "universe", "spacetime", "singularity", "expansion",
            "cosmology", "inertia", "curvature", "force", "dark matter",
            "antimatter", "entropy", "dimension", "big bang", "multiverse",
            "equation", "fields", "mass", "light speed", "strings"}

        # Get the total number of texts
        num_texts = len(self.data)

        # Automatically calculate the number of rows and columns for the pie chart grid layout
        # Number of columns in the grid
        cols = math.ceil(math.sqrt(num_texts))
        # Number of rows in the grid
        rows = math.ceil(num_texts / cols)

        # Set up the figure and axes
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5))
        # Flatten the axes array to make indexing easier
        axes = axes.flatten()

        # Iterate over each document in the data and generate a pie chart
        for i, (label, data) in enumerate(self.data.items()):
            ax = axes[i]

            # Count the occurrences of observation and theory keywords in the document
            word_count = data["wordcount"]
            observation_count = sum(word_count.get(keyword, 0) for keyword in observation_keywords)
            theory_count = sum(word_count.get(keyword, 0) for keyword in theory_keywords)

            # Total number of relevant keywords
            total = observation_count + theory_count
            if total == 0:
                # Handle case with no relevant keywords
                ax.text(0.5, 0.5, "No Relevant Keywords", ha="center", va="center", fontsize=12)
                ax.axis("off")
            else:
                # Otherwise, plot a pie chart of observation vs. theory keywords
                labels = ["Observation", "Theory"]
                values = [observation_count, theory_count]
                colors = ["skyblue", "lightcoral"]
                ax.pie(
                    values,
                    labels=labels,
                    # Show percentage in the pie chart
                    autopct="%1.1f%%",
                    # Start the pie chart from a specific angle
                    startangle=140,
                    # Set the colors for the slices
                    colors=colors,
                    # Style the wedges
                    wedgeprops={'linewidth': 0.5, 'edgecolor': 'black'},
                    # Style the text
                    textprops={'fontweight': 'bold', 'fontsize': 15},
                )
                ax.set_title(label, fontsize=19, fontweight="bold")

        # Turn off any unused axes
        for j in range(num_texts, len(axes)):
            axes[j].axis("off")

        # Adjust layout
        fig.tight_layout()
        plt.show()

    def top_words_bars(self, n=3):
        """
        Get the top N words for each document and their frequencies, normalized by document length.
        Returns a DataFrame where columns are ['Document', 'Word', 'Frequency'].
        """
        data = []

        # Iterate over each document and get the top N words
        for label, doc_data in self.data.items():
            # Total number of words in the document
            total_words = doc_data['numwords']
            # Get the top N most common words
            top_words = doc_data['wordcount'].most_common(n)

            for word, freq in top_words:
                # Normalize frequency by document length
                normalized_freq = freq / total_words
                data.append({'Document': label, 'Word': word, 'Frequency': normalized_freq})

        # Create a DataFrame with the collected data
        top_words_df = pd.DataFrame(data)
        # Call _make_stacked_bars to plot the stacked bar chart
        self._make_stacked_bars(top_words_df)

    def _make_stacked_bars(self, df):
        """
        Plot a bar chart showing the top N words for each document, with each word having its own color.
        Frequencies are normalized by document length to account for varying document sizes.
        """
        def extract_year(doc_label):
            """
            Extract the publication year from the document label (if in the format "Label (Year)").
            """
            if doc_label[-6] == '(' and doc_label[-1] == ')':
                year_str = doc_label[-5:-1]
                if year_str.isdigit():
                    return int(year_str)

        # Apply the extract_year function to each document label and add the year as a new column
        df['Extracted Year'] = df['Document'].apply(extract_year)
        # Sort the DataFrame by the extracted year
        df = df.sort_values('Extracted Year')

        # Pivot the DataFrame to create a matrix of word frequencies
        pivot_df = df.pivot(index='Document', columns='Word', values='Frequency').fillna(0)
        # Ensure documents are in the original order
        pivot_df = pivot_df.loc[df['Document'].unique()]

        # Get all unique words across all documents
        all_words = df['Word'].unique()
        num_colors = len(all_words)

        # Generate a color map with distinct colors for each word
        colors = plt.cm.tab20.colors * (num_colors // len(plt.cm.tab20.colors) + 1)  # Ensure enough colors
        word_colors = {word: colors[i % len(colors)] for i, word in enumerate(all_words)}  # Assign each word a unique color

        # Assign colors to each word in the pivot table for the bar plot
        bar_colors = [word_colors[word] for word in pivot_df.columns]

        # Create the stacked bar chart
        ax = pivot_df.plot(
            kind='bar',
            stacked=True,
            figsize=(12, 8),
            color=bar_colors,
            edgecolor='black')

        # Style the x-axis labels and add titles
        ax.set_xticklabels(pivot_df.index, rotation=35, fontweight='bold')

        # Set the title of the plot with specific font size and weight
        plt.title("Top Words for Each Document (Chronological Order)", fontsize=16, fontweight="bold")
        # Label the x-axis as "Documents" with specific font size and weight
        plt.xlabel("Documents", fontsize=12, fontweight="bold")
        # Label the y-axis as "Word Frequency" with specific font size and weight
        plt.ylabel("Word Frequency", fontsize=12, fontweight="bold")

        # Initialize lists to hold the legend handles and labels
        handles = []
        labels = []

        # Create legend entries for each word with its unique color
        for word, color in word_colors.items():
            # Create a handle for each word (as a colored circle)
            handle = plt.Line2D([0], [0], marker='o', color='w', label=word, markersize=10, markerfacecolor=color)
            # Add the handle to the list
            handles.append(handle)
            # Add the word to the label list
            labels.append(word)

        # Display the legend below the plot with spacing between entries
        plt.legend(
            handles=handles,
            labels=labels,
            # Position the legend below the plot
            bbox_to_anchor=(0.5, -0.3),
            # Place the legend in the upper center
            loc="upper center",
            # Display the legend in 6 columns
            ncol=6,
            # Set the height of the legend handles
            handleheight=2.0,
            # Set the spacing between legend columns
            columnspacing=2.0,
            fontsize=18,
            # Scale the size of the legend markers
            markerscale=1.2,
            # Make the legend text bold
            prop={'weight': 'bold'})

        plt.tight_layout()
        plt.show()