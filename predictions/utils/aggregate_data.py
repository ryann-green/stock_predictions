def rank_data():

    import pandas as pd
    from datetime import datetime
    import warnings

    warnings.filterwarnings('ignore')

    # Load the dataset
    file_path = 'predictions/backtest_results.csv'
    data = pd.read_csv(file_path)

    # Filter to only include rows where predicted_price_higher is True
    filtered_data = data[data['predicted_price_higher'] == True].copy()

    # Convert dates to datetime objects for calculation
    filtered_data['pred_date'] = pd.to_datetime(filtered_data['pred_date'])

    # Define the current date (anchor date)
    current_date = datetime.now()

    # Calculate time difference between current_date and pred_date
    filtered_data['days_since_prediction'] = (current_date - filtered_data['pred_date']).dt.days

    # Define timeframes (in days)
    timeframes = {
        "14": 14,
        "21": 21,
        "30": 30,
        "60": 60,
        "90": 90,
        "180": 180
    }

    # Create a function to assign multiple timeframes for each row
    def assign_multiple_timeframes(days):
        applicable_timeframes = []
        for label, max_days in timeframes.items():
            if days <= max_days:
                applicable_timeframes.append(label)
        return applicable_timeframes

    # Assign multiple timeframes to each row
    filtered_data['applicable_timeframes'] = filtered_data['days_since_prediction'].apply(assign_multiple_timeframes)

    # Explode the rows so that each timeframe gets its own row
    exploded_data = filtered_data.explode('applicable_timeframes')
    exploded_data = exploded_data.rename(columns={'applicable_timeframes': 'timeframe'})

    # Calculate the target price success ratio for each ticker
    success_ratio = (
        data.groupby('ticker')
        .apply(lambda x: (x['first_trigger'] == 'target_price').sum() / len(x))
        .reset_index()
        .rename(columns={0: 'success_ratio'})
    )

    success_ratio['success_ratio_rank']=success_ratio['success_ratio'].rank(ascending=True, method='min').astype(int)

    success_ratio.sort_values('success_ratio',ascending=False).to_csv('rankings/target_success_ratio.csv')

    # Merge success ratio into the exploded data
    exploded_data = exploded_data.merge(success_ratio, on='ticker')

    # Group by ticker and timeframe, calculate the median profit percentage
    aggregated_data = (
        exploded_data.groupby(['ticker', 'timeframe', 'success_ratio'])['profit_pct_per_stock']
        .median()
        .reset_index()
        .rename(columns={'profit_pct_per_stock': 'median_profit_pct'})
    )

    fourteen_day_median_profit_pct=aggregated_data[aggregated_data['timeframe'] == '14'].copy()[['ticker','median_profit_pct','success_ratio']]
    fourteen_day_median_profit_pct['14_day_median_profit_rank']=fourteen_day_median_profit_pct['median_profit_pct'].rank(ascending=True, method='min').astype(int)
    fourteen_day_median_profit_pct['success_ratio_rank']=fourteen_day_median_profit_pct['success_ratio'].rank(ascending=True, method='min').astype(int)

    agg_data_df=fourteen_day_median_profit_pct.sort_values('14_day_median_profit_rank',ascending=False)



    fourteen_30_spread=aggregated_data.pivot(index='ticker', columns='timeframe', values='median_profit_pct')[['14','30']].dropna()
    fourteen_30_spread['14-30_profit_spread']=fourteen_30_spread['14']-fourteen_30_spread['30']
    spread_df=pd.DataFrame(fourteen_30_spread['14-30_profit_spread'])
    spread_df['spread_rank']=spread_df['14-30_profit_spread'].rank(ascending=True, method='min').astype(int)

    merged_df = pd.merge(agg_data_df, spread_df, on='ticker')
    print(merged_df)

    # Pivot the data for bell curvevisualization
    pivot_data = aggregated_data.pivot(index='timeframe', columns='ticker', values='median_profit_pct')
    # Save the processed data for visualization
    # pivot_data.to_csv('rankings/median_profit_pct.csv')
    # aggregated_data.to_csv('rankings/median_profit_pct.csv')

    print(pivot_data.to_csv('rankings/median_profit_bell_pivot.csv'))
    print("Data formatted and saved for visualization. File: formatted_data_with_success_ratio.csv")

    # Prepare for non-trigger rate calc
    backtest_ticker_count=filtered_data.groupby('ticker')['pred_date'].count()
    print(backtest_ticker_count)



    file_path = 'predictions/non_trigger_stocks.csv'
    non_triggers = pd.read_csv(file_path)
    # Filter to only include rows where predicted_price_higher is True
    filtered_non_trigger_data = non_triggers[non_triggers['adj_price_higher'] == True].copy()

    non_triggers_count=filtered_non_trigger_data.groupby('ticker')['last_date'].count()
    # print(non_triggers_count)

    non_trigger_merge= pd.merge(backtest_ticker_count, non_triggers_count, on='ticker')
    non_trigger_merge['all_preds']=non_trigger_merge['pred_date']+non_trigger_merge['last_date']
    non_trigger_merge['non_trigger_rate']=non_trigger_merge['last_date']/non_trigger_merge['all_preds']

    non_trigger_rate=pd.DataFrame(non_trigger_merge['non_trigger_rate'])

    merged_df=pd.merge(merged_df, non_trigger_rate, on='ticker',how='left')
    merged_df['non_trigger_rate']=merged_df['non_trigger_rate'].fillna(0)
    merged_df['non_trigger_rank']=merged_df['non_trigger_rate'].rank(ascending=False, method='min').astype(int)

    # print(merged_df.sort_values('non_trigger_rank',ascending=False))

    # Prepare for latest_prediction rank calc

    file_path = 'predictions/predictions_table.csv'
    predictions = pd.read_csv(file_path)
    max_prediction_date=max(predictions['last_date_for_prediction'])
    # Filter to only include rows where predicted_price_higher is True
    filtered_predictions_data = predictions[(predictions['last_date_for_prediction'] == max_prediction_date) & (predictions['adj_prediction_higher'] == True)].copy()
    max_prediction_date=max(predictions['last_date_for_prediction'])
    filtered_predictions_df=filtered_predictions_data[['ticker','last_date_for_prediction','predicted_higher_success_rate','overall_success_rate']]
    filtered_predictions_df['ranking_mix']=filtered_predictions_df['predicted_higher_success_rate']*.75+filtered_predictions_df['overall_success_rate']*.25
    filtered_predictions_df_clean=filtered_predictions_df[['ticker','last_date_for_prediction','ranking_mix']]

    merged_df=pd.merge(merged_df, filtered_predictions_df_clean, on='ticker',how='left').dropna()
    merged_df['predictions_rank']=merged_df['ranking_mix'].rank(ascending=True, method='min').astype(int)


    final_rankng=merged_df.dropna()[['ticker','14_day_median_profit_rank','success_ratio_rank','spread_rank','non_trigger_rank','predictions_rank']]
    final_rankng.to_csv('rankings/latest_recs.csv')
