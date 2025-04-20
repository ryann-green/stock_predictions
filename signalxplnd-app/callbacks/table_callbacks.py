from dash import Input, Output, dcc
from dash.dash_table import DataTable
from data.data_loader import br_df
from dash.dependencies import Input, Output
import plotly.express as px


def register_table_callbacks(app):
    @app.callback(
            Output("table-container", "children"),  # Use "children" for DataTable
            Output("column-container", "children"),
            Output("line-container", "children"),
            [Input("ticker-filter", "value")]
        )
    def update_table(selected_ticker):
        # Filter the globally loaded data
        filtered_df = br_df[br_df["ticker"] == selected_ticker].sort_values('pred_date',ascending=False)
        
        filtered_df.rename(columns={'ticker': 'Ticker'
                                            , 'pred_date': 'Prediction Date'
                                            , 'overall_success_rate': 'OSR'
                                            ,'predicted_higher_success_rate': 'PHSR'
                                            , 'predicted_price_higher': 'Predicted Higher?'
                                            , 'first_trigger': 'Trigger'
                                            ,'first_trigger_date': 'Trigger Date'
                                            , 'first_trigger_price': 'Trigger Price'
                                            , 'profit_per_stock': '$ Gain/Loss'
                                            , 'profit_pct_per_stock': '% Gain/Loss'}
                                , inplace=True)
        
        pass_through_df=filtered_df[['Prediction Date'
                                    ,'OSR'
                                    ,'PHSR'
                                    ,'Predicted Higher?'
                                    ,'Trigger'
                                    ,'Trigger Date'
                                    ,'Trigger Price'
                                    ,'$ Gain/Loss'
                                    ,'% Gain/Loss']]
        
        pass_through_df.iloc[:, 1] = pass_through_df.iloc[:, 1].round(2)
        pass_through_df.iloc[:, 2] = pass_through_df.iloc[:, 2].round(2)
        pass_through_df.iloc[:, 6] = pass_through_df.iloc[:, 6].round(2)
        pass_through_df.iloc[:, 7] = pass_through_df.iloc[:, 7].round(2)
        pass_through_df.iloc[:, 8] = pass_through_df.iloc[:, 8].round(2)


        
        # sum_gain=pass_through_df.groupby('Trigger').sum('$ Gain/Loss')
        graph_df= filtered_df[filtered_df["Predicted Higher?"] == True]
        bar_df=graph_df.groupby('Trigger', as_index=False).sum('$ Gain/Loss')
        
        col = px.bar(
                bar_df,
                x="Trigger",
                y="$ Gain/Loss",
                color="Trigger",
                title=f"Amount Gained vs Lost by {selected_ticker}",
                # labels={"14_day_median_profit": "Median Profit (%)"},
            )
            
        col.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,  # Adjust height for stacking
        )
        
        line = px.line(
            graph_df,
            x="Prediction Date",
            y="% Gain/Loss",
            # color="Ticker",
            title=f"% Gain/Loss Over Time for {selected_ticker}",
            # labels={"rank_score": "Ranking Score", "last_date_for_prediction": "Date"},
        )

        line.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=300,  # Adjust height for stacking
        )
        
        # Return a DataTable instead of raw data
        return DataTable(
            id="data-table",
            columns=[
                {"name": col, "id": col, "hideable": True} for col in pass_through_df.columns
            ],
            data=pass_through_df.to_dict("records"),
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=13,  
            style_table={
                "overflowX": "auto",
                "maxHeight": "500px",
                "overflowY": "auto",
            },
            style_cell={"textAlign": "center", "padding": "5px"},
            style_data={
            'color': 'black',
            'backgroundColor': 'white'
            },
            style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            }

        ), dcc.Graph(figure=col), dcc.Graph(figure=line)
    