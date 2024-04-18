import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import random

def simulate_user_ratings(final_data):
    """
    Simulates user ratings for meals based on the available meal data.
    
    Parameters:
    final_data (DataFrame): The dataset containing restaurant information with meals.
    
    Returns:
    DataFrame: User-item interaction matrix.
    """
    meal_ids = final_data['Meal name'].unique().tolist()
    user_ratings = {}

    for user_id in range(1, 1001):  # Simulate ratings for 1000 users
        ratings = {meal: np.nan for meal in meal_ids}  # Start with all NaN ratings
        num_ratings = random.randint(50, min(len(meal_ids), 150))  # Number of meals each user will rate
        rated_meals = random.sample(meal_ids, num_ratings)

        for meal in rated_meals:
            ratings[meal] = random.uniform(0, 5)  # Assign a random rating between 0 and 5

        user_ratings[user_id] = ratings

    # Convert to DataFrame
    ratings_df = pd.DataFrame.from_dict(user_ratings, orient='index')
    ratings_df.index.name = 'User ID'
    return ratings_df

def normalize(pred_ratings):
    """
    Normalizes the prediction ratings.
    """
    return (pred_ratings - pred_ratings.min()) / (pred_ratings.max() - pred_ratings.min())

def generate_prediction_df(user_item_matrix, n_factors=10):
    """
    Generates predicted ratings using matrix factorization (SVD).
    
    Parameters:
    user_item_matrix (DataFrame): User-item interaction matrix.
    n_factors (int): Number of singular values and vectors to compute.
    
    Returns:
    DataFrame: Predicted ratings DataFrame.
    """
    mat = csr_matrix(user_item_matrix.fillna(0).values)  # Fill NA with 0 and convert to CSR matrix

    if not 1 <= n_factors < min(mat.shape):
        raise ValueError("Must be 1 <= n_factors < min(mat.shape)")

    u, s, v = svds(mat, k=n_factors)
    s_diag_matrix = np.diag(s)
    pred_ratings = np.dot(np.dot(u, s_diag_matrix), v)
    pred_ratings = normalize(pred_ratings)

    pred_df = pd.DataFrame(
        pred_ratings,
        index=user_item_matrix.index,
        columns=user_item_matrix.columns
    )
    return pred_df.transpose()

def recommend_meals(final_data):
    """
    Generates a complete recommendation for all meals based on simulated user ratings and matrix factorization.
    
    Parameters:
    final_data (DataFrame): The processed dataset containing meal and restaurant data.
    
    Returns:
    DataFrame: DataFrame containing predictions for each user.
    """
    user_item_matrix = simulate_user_ratings(final_data)
    predictions = generate_prediction_df(user_item_matrix)
    return predictions
