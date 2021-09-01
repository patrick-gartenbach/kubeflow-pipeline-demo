from typing import NamedTuple
import kfp.components as comp

def test_xgboost(test_data_path: comp.InputPath("CSV"),label_column_name,model_path: comp.InputPath("XGBoost Model"))-> NamedTuple('Outputs', [('mlpipeline_metrics', 'Metrics'),]):
    import pandas as pd
    import xgboost as xgb
    from sklearn.metrics import mean_squared_error,r2_score
    import numpy as np 
    import json

    test = pd.read_csv(test_data_path)
    x = test.drop(columns=[label_column_name])
    y = test[label_column_name]
    xgb_model = xgb.XGBRegressor()
    xgb_model.load_model(model_path)
    xgb_preds = xgb_model.predict(x)
    rsme = np.sqrt(mean_squared_error(y, xgb_preds))
    r2 = r2_score(y, xgb_preds)

    print("R2 XGB:",r2)
    print("RSME XGB:",rsme)
    metrics = {
        'metrics': [
            {
              'name': 'r2-score-testdata', # The name of the metric. Visualized as the column name in the runs table.
              'numberValue':  r2, # The value of the metric. Must be a numeric value.
              'format': "RAW",   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            },
            {
              'name': 'rsme-score-testdata', # The name of the metric. Visualized as the column name in the runs table.
              'numberValue':  rsme, # The value of the metric. Must be a numeric value.
              'format': "RAW",   # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            },
            ]
    }
    return [json.dumps(metrics)]