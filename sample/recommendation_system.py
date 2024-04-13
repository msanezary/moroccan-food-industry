import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error

def load_data(filepath):
    return pd.read_csv(filepath)

def create_interaction_matrix(df, user_col, item_col, rating_col, threshold=None):
    interactions = df.groupby([user_col, item_col])[rating_col].sum().unstack().reset_index().fillna(0).set_index(user_col)
    if threshold is not None:
        interactions = interactions.applymap(lambda x: 1 if x > threshold else 0)
    return interactions

def perform_svd(interaction_matrix, n_factors=100):
    matrix = csr_matrix(interaction_matrix.values)
    u, s, vt = svds(matrix, k=n_factors)
    s_diag_matrix = np.diag(s)
    X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
    return X_pred

def calculate_mse(actual, predicted):
    mse = mean_squared_error(actual, predicted)
    return mse

def setup_recommendation_system(filepath, user_col, item_col, rating_col, n_factors=100, threshold=None):
    data = load_data(filepath)
    interaction_matrix = create_interaction_matrix(data, user_col, item_col, rating_col, threshold)
    predicted_ratings = perform_svd(interaction_matrix, n_factors)
    mse = calculate_mse(interaction_matrix.values, predicted_ratings)
    print(f'Mean Squared Error of the recommendation system: {mse}')

if __name__ == "__main__":
    filepath = 'path_to_ratings_data.csv'
    setup_recommendation_system(filepath, 'user_id', 'item_id', 'rating')
