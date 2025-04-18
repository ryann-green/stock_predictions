from .table_callbacks import register_table_callbacks
from .scatter_callbacks import register_scatter_callbacks
from .ranking_callbacks import register_ranking_callbacks
from .collapsible_callbacks import register_collapsible_callbacks

def register_callbacks(app):
    register_table_callbacks(app)
    register_scatter_callbacks(app)
    register_ranking_callbacks(app)
    register_collapsible_callbacks(app)