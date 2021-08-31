import kfp.components as comp
def train_xgboost(train_data_path: comp.InputPath("CSV"),label_column_name,model_path: comp.OutputPath("XGBoost Model")):
    import pandas as pd
    import xgboost as xgb
    train = pd.read_csv(train_data_path)
    x = train.drop(columns=[label_column_name])
    y = train[label_column_name]
    xgb_model = xgb.XGBRegressor()
    xgb_model.fit(x,y)
    xgb_model.save_model(model_path)