import dash_bootstrap_components as dbc
from layout.welcome_section import create_welcome_section
from layout.weighting_controls import create_weighting_controls
from layout.cards import create_cards
from layout.ranked_table import create_ranked_table
from layout.scatter_plot import create_scatter_plot
from layout.filtered_table import create_filtered_table
from layout.line_chart import create_line_chart
from layout.column_chart import create_column_chart
from data.data_loader import br_df,p_df


def create_layout():
    return dbc.Container(
        [   create_welcome_section(),
            # create_data_summary(br_df,p_df),
            dbc.Row(
                [
                    dbc.Col(create_weighting_controls(), width=6),
                    dbc.Col(create_cards(), width=6)
                 ]
            ),
            dbc.Row(
                [
                    dbc.Col(create_ranked_table(),width=6),
                    dbc.Col(create_filtered_table(br_df), width=6),
                     
                    
                ]
            ),
            dbc.Row(
                [
                      # Container 3: Filtered Data Table
                    dbc.Col(create_scatter_plot(p_df), width=6),
                    dbc.Col(
                    dbc.Container(
                        [
                            create_line_chart(),
                            create_column_chart(),
                           
                        ],
                        className="my-3 p-3 bg-light border rounded"
                    ),
                    width=6,  # Left side: Charts stacked
            ),
                     # Container 2: Scatter Plot
                    
                ]   
            ),
        ],
        fluid=True,
        className="p-2 mt-2 mb-2",  # Adds padding and margin
        style={"maxWidth": "1400px", "margin": "auto"}  # Centers content
    )



    





    

   
    
    