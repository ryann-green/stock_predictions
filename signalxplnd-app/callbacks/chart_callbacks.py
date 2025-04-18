from dash import Input, Output, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from data.data_loader import load_data  
from dash.dependencies import Input, Output, State
import plotly.express as px