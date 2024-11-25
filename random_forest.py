import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, LeaveOneOut
import numpy as np
def test_models(df_predictor, df_target, n_trees):
    model = RandomForestRegressor(n_estimators=n_trees, random_state=42)
    scores = cross_val_score(model, df_predictor, df_target, cv=LeaveOneOut(), scoring='neg_mean_absolute_error')  
    return -np.mean(scores)
def main():

    
    target_path = 'train_predict.csv'
    target_pd = pd.read_csv(target_path)
    target_df = target_pd["y"]  

    raw_path = 'train_raw.csv'
    raw_df = pd.read_csv(raw_path)
    
    normalized_path = 'train_normalized.csv'
    normalized_df = pd.read_csv(normalized_path)
    
    pca_path = 'train_normalized.csv'
    pca_df = pd.read_csv(pca_path)
    
    fourrier_path =  'train_fourrier.csv'
    fourrier_df = pd.read_csv(fourrier_path)
    
    
    data = {
    'R': [test_models(raw_df, target_df, 200), test_models(raw_df, target_df, 400), test_models(raw_df, target_df, 800)],
    'N': [test_models(normalized_df, target_df, 200), test_models(normalized_df, target_df, 400), test_models(normalized_df, target_df, 800)],
    'P': [test_models(pca_df, target_df, 200), test_models(pca_df, target_df, 400), test_models(pca_df, target_df, 800)],
    'F': [test_models(fourrier_df, target_df, 200), test_models(fourrier_df, target_df, 400), test_models(fourrier_df, target_df, 800)]
}
    indices = ['200', '400', '800']  


    df = pd.DataFrame(data, index=indices)


    df.to_csv('dados.csv', index=True)
    
main()


