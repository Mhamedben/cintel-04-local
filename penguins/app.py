import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req

# Provides the Palmer Penguins dataset
import palmerpenguins

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Title to main page
ui.page_opts(title="Penguin Data MhamedM", fillable=True)

# creates sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h5("Sidebar")
    
# Create a dropdown input to choose a column
    ui.input_selectize(
        "selected_attribute","Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 40)

# Use ui.input_slider() to create a slider input for the number of Seaborn bins
ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 40, 20)

# Added a horizontal rule
ui.hr()

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species
ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

# Creates a checkbox group input for islands
ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=True,
    )

# Use ui.a() to add a hyperlink to the sidebar
ui.a(
        "Mhamedben's GitHub Repo",
        href="https://github.com/Mhamedben/cintel-03-data/blob/main/app.py",
        target="_blank",
    )

 
# create a layout to include 2 cards with a data table and data grid
with ui.layout_columns():
    with ui.card(full_screen=True): 
# full_screen option to view expanded table/grid
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data())

# Expanded table/grid
    with ui.card(full_screen=True):  
        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())



# Creates a Plotly Histogram showing all species

    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")
    
        @render_plotly
        def plotly_histogram():
          return px.histogram(
          filtered_data(), 
          x=input.selected_attribute(), 
          nbins=input.plotly_bin_count(),
          color="species",
          )     


# Creates a Seaborn Histogram showing all species

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram")

        palette = sns.color_palette("Set3")  # Choose a palette with 3 colors

        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
          histplot = sns.histplot(filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count(), hue="species", palette=palette)
          histplot.set_title("Palmer Penguins MhamedM")
          histplot.set_xlabel("Body Mass (g)")  # Set x-axis label
          histplot.set_ylabel("Count")  # Set y-axis label
          return histplot


# Creates a Plotly Scatterplot showing all species and islands

    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species and islands")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(filtered_data(),
                x="bill_length_mm",
                y="body_mass_g",
                color="species",
                facet_col="island",  # Add facet_col parameter to separate scatterplots by island
                title="Penguins Plot MhamedM",
                labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            }, 
        )
# Creates a Plotly Boxplot showing all species and islands
    with ui.card(full_screen=True):
        ui.card_header("Plotly Boxplot: Species")

        @render_plotly
        def plotly_boxplot():
            return px.box(filtered_data(),
                x="species",
                y=input.selected_attribute(),
                color="island", #Add a color parameter to differentiate boxplots by island
                title="Penguins Boxplot MhamedM",
                labels={
                    "species": "Species",
                    input.selected_attribute(): input.selected_attribute().replace("_", " ").title(),
                },
            )
# Reactive calculations and effects#

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

# Reactive calculation to filter data based on selected species and islands

@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))
    ]
