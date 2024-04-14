import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error
import sys

def load_data(filepath):
    """
    Loads data from a CSV file into a pandas DataFrame.
    
    Parameters:
    filepath (str): The path to the CSV file.
    
    Returns:
    DataFrame: The loaded data.
    """
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        sys.exit(1)

def generate_user_item_matrix(df, user_col, item_col, rating_col, threshold=None):
    """
    Creates an interaction matrix from a DataFrame.

    Parameters:
    df (DataFrame): The dataset containing the user-item interactions.
    user_col (str): Column name for user IDs.
    item_col (str): Column name for item IDs.
    rating_col (str): Column name for ratings.
    threshold (int, optional): Threshold value to binarize the ratings.

    Returns:
    DataFrame: The interaction matrix.
    """
    try:
        interactions = df.groupby([user_col, item_col])[rating_col].sum().unstack().reset_index().fillna(0).set_index(user_col)
        if threshold is not None:
            interactions = interactions.applymap(lambda x: 1 if x > threshold else 0)
        return interactions
    except Exception as e:
        print(f"Error creating interaction matrix: {e}")
        return pd.DataFrame()

def generate_prediction_df(interaction_matrix, n_factors=100):
    """
    Performs Singular Value Decomposition on the interaction matrix.

    Parameters:
    interaction_matrix (DataFrame): The user-item interaction matrix.
    n_factors (int): Number of singular values and vectors to compute.

    Returns:
    np.array: The matrix approximated from the SVD operation.
    """
    try:
        matrix = csr_matrix(interaction_matrix.values)
        u, s, vt = svds(matrix, k=n_factors)
        s_diag_matrix = np.diag(s)
        X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
        mse = mean_squared_error(interaction_matrix.values, X_pred)
        print(f'Mean Squared Error of the recommendation system: {mse}')
        return X_pred
    except Exception as e:
        print(f"Error performing SVD or calculating MSE: {e}")
        return np.array([])

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'path_to_ratings_data.csv'
    data = load_data(filepath)
    user_item_matrix = generate_user_item_matrix(data, 'user_id', 'item_id', 'rating')
    prediction_results = generate_prediction_df(user_item_matrix, 100)
