import panel as pn
from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature
import plotly.express as px
import plotly.graph_objects as go


class FeatureOneYear(ParentGeovizFeature):
    def getOptionName(self):
        return "one_year"

    def getRequiredColumns(self):
        return ["time_column", "latitude_column", "longitude_column"]

    def getHeaderText(self):
        return "One Year Map"

    def _generateComponent(self):
        desired_year_num = pn.widgets.IntInput(
            name="Enter Year",
            start=self.df["Year"].min(),
            end=self.df["Year"].max(),
            value=self.df["Year"].median().astype("int32"),
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
            victim_dropdown = pn.widgets.Select(
                value=unique_values[0], options=unique_values
            )

            one_year_plot = pn.bind(
                self._update_one_year_plot,
                new_df=self.df,
                year_value=desired_year_num,
                filter_value=victim_dropdown,
            )

            # Display the dropdowns and initial plot
            one_year = pn.Column(
                desired_year_num,
                victim_dropdown,
                pn.pane.Plotly(one_year_plot, sizing_mode="stretch_width"),
            )
        else:
            one_year_plot = pn.bind(
                self._update_one_year_plot,
                new_df=self.df,
                year_value=desired_year_num,
                filter_value="All",
            )

            # Display the dropdowns and initial plot
            one_year = pn.Column(
                desired_year_num,
                pn.pane.Plotly(one_year_plot, sizing_mode="stretch_width"),
            )

        return one_year

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

    def _update_one_year_plot(self, new_df, year_value, filter_value):
        filtered_df = new_df[new_df["Year"] == year_value]
        if filter_value != "All":
            column_name = self.featureCustomizations["filter_one_year_column"]
            filtered_df = filtered_df[filtered_df[column_name] == filter_value]

        if filtered_df.empty:
            return self._emptyScattermap()

        if "hover_text_columns" in self.featureCustomizations:
            fig = px.scatter_mapbox(
                filtered_df,
                lat=self.latitude_column_name,
                lon=self.longitude_column_name,
                hover_name=self.time_column_name,
                hover_data=self.featureCustomizations["hover_text_columns"],
                color="Month",
                color_discrete_sequence=px.colors.qualitative.Light24,
                zoom=1,
                height=400,
            )
        else:
            fig = px.scatter_mapbox(
                filtered_df,
                lat=self.latitude_column_name,
                lon=self.longitude_column_name,
                color="Month",
                color_discrete_sequence=px.colors.qualitative.Light24,
                zoom=1,
                height=400,
            )
        fig.update_layout(
            mapbox_style="open-street-map", margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )

        return fig
