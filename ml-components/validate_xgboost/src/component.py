from typing import NamedTuple
import kfp.components as comp
def validate_xgboost(train_data_path: comp.InputPath("CSV"),test_data_path: comp.InputPath("CSV"),label_column_name,model_path: comp.InputPath("XGBoost Model"))-> NamedTuple('Outputs', [('mlpipeline_metrics', 'Metrics'),]):
    import pandas as pd
    import xgboost as xgb
    from sklearn.metrics import mean_squared_error,r2_score
    from sklearn.model_selection import cross_validate,KFold
    import numpy as np 
    import json
    train = pd.read_csv(train_data_path)
    test = pd.read_csv(test_data_path)
    data = pd.concat([train, test], ignore_index=True, sort=False)
    x = data.drop(columns=[label_column_name])
    y = data[label_column_name]
    xgb_model = xgb.XGBRegressor()
    xgb_model.load_model(model_path)
    validation_results = cross_validate(xgb_model,x,y,cv=KFold(shuffle=True,random_state=42),scoring=('r2','neg_root_mean_squared_error')) 
    r2 = np.mean(validation_results['test_r2'])
    rsme = np.abs(np.mean(validation_results['test_neg_root_mean_squared_error']))          
    print("R2 XGB:",r2)
    print("RSME XGB:",rsme)
    metrics = {
        'metrics': [
            {
              'name': 'r2-score-crossval', # The name of the metric. Visualized as the column name in the runs table.
              'numberValue': r2, # The value of the metric. Must be a numeric value.
              'format': "RAW",   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            },
            {
              'name': 'rsme-score-crossval', # The name of the metric. Visualized as the column name in the runs table.
              'numberValue':  rsme, # The value of the metric. Must be a numeric value.
              'format': "RAW",   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            },
            ]
    }
    return [json.dumps(metrics)]