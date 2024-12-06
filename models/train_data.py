import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression

def prep_train_test_data(data,feature_cols,target_col):
        # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data[feature_cols], data[target_col], test_size=0.2, random_state=42)

    # # # Feature selection using SelectKBest
    k_best_features = SelectKBest(f_regression, k=10)
    

    X_train_selected = k_best_features.fit_transform(X_train, y_train)
    X_test_selected = k_best_features.transform(X_test)

    # # # Get the selected feature names
    selected_feature_names = [feature_cols[i] for i in k_best_features.get_support(indices=True)]
    print(selected_feature_names)

    # # # Convert X_train_selected and X_test_selected back to DataFrames for easier manipulation
    X_train_selected_df = pd.DataFrame(X_train_selected, index=X_train.index, columns=selected_feature_names).sort_index(ascending=True)
    # print(X_train_selected_df)
    X_test_selected_df = pd.DataFrame(X_test_selected, index=X_test.index, columns=selected_feature_names).sort_index(ascending=True)
    
    return X_train_selected_df,X_test_selected_df,y_train,y_test,selected_feature_names