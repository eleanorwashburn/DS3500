"""
HW 3 - Dashboards
Liam Thompson and Eleanor Washburn
October 15th, 2024
"""
# Import needed libraries
from happiness_report_api import HappinessAPI, initialize_database
import panel as pn
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from sankey import make_sankey
import random

# Initialize the SQLite database with the CSV file
initialize_database()

# Create an instance of HappinessAPI
api = HappinessAPI()

# Load resources for Panel widgets and plots to work
pn.extension()

# Create a widget to allow users to search for a country
country_search = pn.widgets.AutocompleteInput(
    name='Search (Case-Sensitive)',
    options=api.get_countries(),
    placeholder='Type to search...')

# Define a widget for an alphabetical for alphabetical country list
country_select = pn.widgets.Select(name='Select from List', options=api.get_countries())

# Sync the search input and dropdown selection
@pn.depends(country_search, watch=True)
def update_dropdown(search_value):
    if search_value in country_select.options:
        country_select.value = search_value

@pn.depends(country_select, watch=True)
def update_search_dropdown(selected_value):
    country_search.value = selected_value

# Define widgets for adjusting plot dimensions
image_width_slider = pn.widgets.IntSlider(name='Width', start=400, end=1200, value=650, step=10)
image_height_slider = pn.widgets.IntSlider(name='Height', start=300, end=800, value=500, step=10)

def get_data(country):
    """For the selected country, return its data"""
    data = api.get_data_by_country(country)
    return data

# Define the plotting function for metrics over time
metrics_select = pn.widgets.MultiChoice(
    name='Select Happiness Metrics',
    options= api.get_happiness_factors(),
    value = list(random.sample(api.get_happiness_factors(), 1))) #Setting default values when generated

@pn.depends(country_select, metrics_select, image_width_slider, image_height_slider)
def plot_metrics_over_time(country, metrics, width, height):
    """For a given country, plots the selected happiness metrics over time."""
    # Get the data for selected countries
    data = get_data(country)

    # Create the plot
    fig, ax = plt.subplots(figsize=(width / 100, height / 100))
    for metric in metrics:
        if metric in data.columns:
            ax.plot(data['year'], data[metric], label=metric)
    ax.set_title(f'Metrics for {country} Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Metric Value')
    ax.legend()

    # Close the figure after plotting
    plt.close(fig)

    # Return the figure
    return fig

# Initialize the MultiChoice widget for selecting happiness metrics
sankey_metrics_select = pn.widgets.MultiChoice(
    name='Select Happiness Metrics',
    options= api.get_happiness_factors(exclude_life_ladder=True),
    value= list(random.sample(api.get_happiness_factors(exclude_life_ladder=True), 7))) #Setting default values when generated

@pn.depends(country_select, sankey_metrics_select, image_width_slider, image_height_slider)
def plot_sankey_diagram(country, metrics, width, height):
    """Creates a sankey diagram for a chosen country that shows the relative impact of a selected metrics on the
       country's happiness
    """
    # Get the data for selected countries
    data = get_data(country)

    # Calculate correlations with Happiness Score
    correlations = data[['Life Ladder'] + metrics].corr().loc[metrics, 'Life Ladder'].abs()
    values = correlations.values.tolist()

    # Prepare the dataframe for the sankey diagram
    df = pd.DataFrame({
        'Source': metrics,
        'Target': ['Happiness'] * len(metrics),
        'Value': values})

    # Use make_sankey to create the diagram
    fig = make_sankey(df, src='Source', targ='Target', vals='Value', width=width, height=height)
    fig.update_layout(title_text=f"Sankey Diagram: Impact of Metrics on Happiness in {country}")

    # Return the Plotly figure wrapped in Panel
    return pn.pane.Plotly(fig)

# Initialize the MultiChoice widget for selecting countries
country_compare_select = pn.widgets.MultiChoice(
    name='Select Countries for Comparison',
    options=api.get_countries(),
    value = random.sample(api.get_countries(), 3)) #Setting default values when generated

# Initialize the MultiChoice widget for selecting happiness metrics
metrics_compare_select = pn.widgets.MultiChoice(
    name='Select Happiness Metrics for Comparison',
    options= api.get_happiness_factors(),
    value= list(random.sample(api.get_happiness_factors(), 5))) #Setting default values when generated


@pn.depends(country_compare_select, metrics_compare_select, image_width_slider, image_height_slider)
def plot_comparison_chart(countries, metrics, width, height):
    """Creates a dynamic bar chart that compares a selected number of metrics for a selected number of countries"""
    # Get the data for selected countries
    data_frames = [get_data(country) for country in countries]

    # Filter out empty data frames
    data_frames = [df for df in data_frames if not df.empty]

    # Combine data into a single DataFrame
    combined_data = pd.concat(data_frames)

    # Prepare data for visualization
    comparison_data = combined_data[['Country name', 'Life Ladder'] + metrics]

    # Create a bar chart for comparison
    fig = go.Figure()

    for country in countries:
        country_data = comparison_data[comparison_data['Country name'] == country]
        fig.add_trace(go.Bar(
            x=metrics,
            y=country_data[metrics].values.flatten(),
            name=country))

    # Update layout to accommodate width and height
    fig.update_layout(
        title_text='Comparison of Happiness Metrics for: ' + ', '.join(countries),
        barmode='group',
        xaxis_title='Metrics',
        yaxis_title='Values',
        width=width,
        height=height)

    # Return the Plotly figure wrapped in Panel
    return pn.pane.Plotly(fig)

def create_plot_card(title, plot_function, *metrics_selectors):
    """
    Creates a plot card with a title, metrics selector, and a plot function."""
    # Create a list of the metrics selectors
    metrics_layout = [metrics_selector for metrics_selector in metrics_selectors]

    # Create a column with the title and metrics selectors
    return pn.Column(
        pn.pane.Markdown(f'## {title}'),
        *metrics_layout,
        plot_function)

# Call each card into the create_plot_card function
plot_over_time_card = create_plot_card('Metrics Over Time', plot_metrics_over_time, metrics_select)
sankey_card = create_plot_card('Sankey Diagram', plot_sankey_diagram, sankey_metrics_select)
comparison_card = create_plot_card('Happiness Comparisons', plot_comparison_chart, country_compare_select, metrics_compare_select)

# Create the sidebar
sidebar = pn.Column(
    pn.pane.Markdown("## Select Country"),
    country_search,
    country_select,
    pn.pane.Markdown("## Adjust Plot Dimensions"),
    image_width_slider,
    image_height_slider)

# Define the layout using FastListTemplate
layout = pn.template.FastListTemplate(
    title='World Happiness Report',
    sidebar=sidebar,
    theme_toggle=False,
    main=[
        pn.Tabs(
            ('Metrics Over Time', plot_over_time_card),
            ('Sankey Diagram', sankey_card),
            ('Happiness Comparisons', comparison_card),
            active=0)],
    header_background='#FFC000')

# Display the layout
layout.servable()
layout.show()
