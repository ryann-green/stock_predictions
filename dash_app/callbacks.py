# Place all functional callbacks from the app in this script. 
# Each callback will be called when triggered by the app when the status is changed.

from dash import Input, Output,dcc
import dash_bootstrap_components as dbc

def register_callbacks(app):
    @app.callback(
        Output("table-container", "children"),
        [Input("ticker-filter", "value")]
    )
    def update_table(selected_ticker):
        from data_loader import load_data
        df = load_data()
        filtered_df = df[df["ticker"] == selected_ticker]
        return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    
    @app.callback(
        Output("scatter-container", "children"),
        [Input("ticker-filter", "value")]
    )
    def update_scatter(selected_ticker):
        from data_loader import load_data
        import plotly.express as px

        df = load_data()
        filtered_df = df[df["ticker"] == selected_ticker]
        
        fig = px.scatter(data_frame=filtered_df,
                    x="predicted_higher_success_rate",
                    y="overall_success_rate",
                    color="profit_pct_per_stock",
                    hover_name='ticker',
                    title="Predicted Higher Success vs Overall Success")

        fig.update_layout(transition_duration=500)
        
        
        return dcc.Graph(figure=fig)
