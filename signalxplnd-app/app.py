import dash 
import dash_bootstrap_components as dbc
from layout.layout import create_layout
from callbacks import register_callbacks

# Create Dash app ONCE at the module level
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    requests_pathname_prefix="/dev/",
    title="SignalXplnd"
)

# Set app layout and register callbacks ONCE
app.layout = create_layout()
register_callbacks(app)

# Expose the underlying Flask server for WSGI
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
