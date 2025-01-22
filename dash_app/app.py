import dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set app layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
