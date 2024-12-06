def generate_lead_features (data,days_ahead):
        
            # # Generate lead features for the past 30 days
        # Shift (i) positive means that the data from the previous "i" day prior to the current row will be reflected in the lead_i column 
        lead_features = []

        for i in range(1, days_ahead):
            
            cols=['Close', 'ALMA', 'Stochastic_RSI', 'Williams_%R', 'ROC']
            
            # add each day close and volume change as additional columns to evaluate for features
            for n in range(1, days_ahead):
                cols.append(f'{n}_Day Close Change')
                cols.append(f'{n}_Day Volume Change')
            
            leads = data[cols].shift(i)
            leads.columns = [f'{col}_lead_{i}' for col in leads.columns]
            lead_features.append(leads)
            
            return lead_features