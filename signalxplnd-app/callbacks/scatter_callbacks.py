from dash import Input, Output, dcc

from data.data_loader import p_df  
from dash.dependencies import Input, Output
import plotly.express as px


def register_scatter_callbacks(app):
    @app.callback(
        Output("scatter-container", "children"),  # Use "children" for dcc.Graph
        [Input("date-filter", "value")]
    )
    def update_scatter(selected_date):

        # Filter the globally loaded data
        filtered_df = p_df[p_df["last_date_for_prediction"] == selected_date]
        
        # Generate the scatter plot
        fig = px.scatter(
            data_frame=filtered_df,
            x="predicted_higher_success_rate",
            y="overall_success_rate",
            color="adj_prediction_higher",
            hover_name="ticker",
            title=f"Predicted Higher Success vs Overall Success for {selected_date}",
        )

        fig.update_layout(transition_duration=500)
        
        # Return a Graph component
        return dcc.Graph(figure=fig)
    