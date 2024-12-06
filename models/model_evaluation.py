import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np


def evaluate_models (model_items,days_ahead,X_train_selected_df,X_test_selected_df,y_train,y_test,predictions_df):
        # # # Train and evaluate each model
        results = {}
        
        for model_name, model in model_items:
        
            model.fit(X_train_selected_df, y_train)
            predictions = model.predict(X_test_selected_df)
            
        #     # Create a DataFrame for predictions with the same index as the training set
            predictions_train = pd.DataFrame(model.predict(X_train_selected_df), index=X_train_selected_df.index, columns=[f'{model_name}_Predicted_Close_{days_ahead}d_ahead'])
            # print(predictions_train)

        #     # Merge the predictions with the predictions_df DataFrame
            predictions_df = predictions_df.merge(predictions_train, left_index=True,right_index=True, how='left')
            
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            results[model_name] = rmse
            print(f'{model_name} RMSE: {rmse}')
            
        return results, predictions_df