import pandas as pd
import matplotlib.pyplot as plt
import panel as pn
import seaborn as sns
from IPython.display import display

from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature


class FeatureSearch(ParentGeovizFeature):
    def getOptionName(self):
        return "search_columns"

    def getRequiredColumns(self):
        return []

    def getHeaderText(self):
        return "Search Key Terms in Columns"

    def _generateComponent(self):
        # Define the search bar widgets
        column_dropdown = pn.widgets.Select(
            options=list(self.df.columns), name="Column"
        )

        search_textbox = pn.widgets.TextInput(name="Search term")

        # Register the update function with the widgets
        plot = pn.bind(
            self._update_search,
            column=column_dropdown,
            search_term=search_textbox,
        )
        search = pn.Column(column_dropdown, search_textbox, plot)

        return search

    def get_unique_values(self, column):
        return self.df[column].unique().tolist()

    # Define the search function
    def search_data(self, column, search_term):
        filtered_df = self.df[
            self.df[column].str.contains(search_term, case=False, na=False)
        ]
        return filtered_df

    # Define the update function
    def _update_search(self, column, search_term=""):
        if search_term == "":
            return pn.Column(pn.pane.Matplotlib(sizing_mode="stretch_width"))
        filtered_df = self.search_data(column, search_term)

        num_columns = len(filtered_df[column].value_counts())
        height = max(6, num_columns * 0.5)
        # Plot the results
        fig, ax = plt.subplots(figsize=(12, height))
        sns.countplot(
            y=column,
            data=filtered_df,
            order=filtered_df[column].value_counts().index,
            ax=ax,
        )
        for p in ax.patches:
            ax.annotate(
                p.get_width(),
                (p.get_x() + p.get_width() + 20, p.get_y() + 0.4),
                ha="left",
                va="center",
            )
        ax.set_title("Occurrences of " + search_term + " in column: " + column)
        ax.set_xlabel("Count")
        ax.set_ylabel(column)

        plt.tight_layout()

        # Display the plot
        return pn.Column(pn.pane.Matplotlib(fig, sizing_mode="stretch_width"))
