import panel as pn
from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature
import plotly.express as px
import plotly.graph_objects as go


class FeatureYearlyRange(ParentGeovizFeature):
    def getOptionName(self):
        return "yearly_range"

    def getRequiredColumns(self):
        return ["time_column", "latitude_column", "longitude_column"]

    def getHeaderText(self):
        return "Year Range Map"

    def _generateComponent(self):
        year_range_slider = pn.widgets.RangeSlider(
            name="Select Year Range",
            start=self.df["Year"].min(),
            end=self.df["Year"].max(),
            value=(self.df["Year"].min(), self.df["Year"].max()),
            step=1,
        )

        # If we have a filter column, add that. Otherwise, don't.
        if "filter_one_year_column" in self.featureCustomizations:
            unique_values = (
                self.df[self.featureCustomizations["filter_one_year_column"]]
                .value_counts()
                .index.tolist()
            )

            unique_values = ["All"] + unique_values
            # Create a dropdown widget with unique victim values
            value_dropdown = pn.widgets.Select(
                value=unique_values[0], options=unique_values
            )

            yearly_range_plot = pn.bind(
                self._update_yearly_range_plot,
                new_df=self.df,
                years_value=year_range_slider,
                filter_value=value_dropdown,
            )

            # Display the dropdowns and initial plot
            yearly_range = pn.Column(
                year_range_slider,
                value_dropdown,
                pn.pane.Plotly(yearly_range_plot, sizing_mode="stretch_width"),
            )

        else:
            yearly_range_plot = pn.bind(
                self._update_yearly_range_plot,
                new_df=self.df,
                years_value=year_range_slider,
                filter_value="All",
            )

            yearly_range = pn.Column(
                year_range_slider,
                pn.pane.Plotly(yearly_range_plot, sizing_mode="stretch_width"),
            )

        return yearly_range

    def _emptyScattermap(self):
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 20, "t": 20, "l": 20, "b": 20},
            annotations=[
                {
                    "text": "No Points Found",
                    "x": 0.5,
                    "y": 0.5,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 18},
                }
            ],
        )
        return fig

    def _update_yearly_range_plot(self, new_df, years_value, filter_value):
        min_year, max_year = years_value
        filtered_df = new_df[
            (new_df["Year"] >= min_year) & (new_df["Year"] <= max_year)
        ]
        if filter_value != "All":
            column_name = self.featureCustomizations["filter_one_year_column"]
            filtered_df = filtered_df[filtered_df[column_name] == filter_value]

        if filtered_df.empty:
            return self._emptyScattermap()

        if "hover_text_columns" in self.featureCustomizations:
            fig = px.scatter_mapbox(
                filtered_df,
                lat="latitude",
                lon="longitude",
                hover_name="date",
                hover_data=self.featureCustomizations["hover_text_columns"],
                color="Year",
                zoom=1,
                height=400,
            )
        else:
            fig = px.scatter_mapbox(
                filtered_df,
                lat=self.latitude_column_name,
                lon=self.longitude_column_name,
                color="Year",
                zoom=1,
                height=400,
            )
        fig.update_layout(
            mapbox_style="open-street-map", margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )
        return fig
