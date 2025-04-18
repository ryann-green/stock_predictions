from dash.dependencies import Input, Output, State

def register_collapsible_callbacks (app):

# Callbacks to toggle collapsible sections
    @app.callback(
        Output("ranking-collapse", "is_open"),
        Input("ranking-button", "n_clicks"),
        State("ranking-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_ranking(n_clicks, is_open):
        return not is_open  

    @app.callback(
        Output("features-collapse", "is_open"),
        Input("features-button", "n_clicks"),
        State("features-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_features(n_clicks, is_open):
        return not is_open  
    