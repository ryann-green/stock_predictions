from .table_callbacks import register_table_callbacks
from .scatter_callbacks import register_scatter_callbacks
from .ranking_callbacks import register_ranking_callbacks
from .collapsible_callbacks import register_collapsible_callbacks
from .card_callbacks import register_card_callbacks

def register_callbacks(app):
    register_table_callbacks(app)
    register_scatter_callbacks(app)
    register_ranking_callbacks(app)
    register_collapsible_callbacks(app)
    register_card_callbacks(app)