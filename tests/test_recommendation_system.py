import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from recommendation_system import simulate_user_ratings, generate_prediction_df, recommend_meals

class TestRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Sample data mimicking the final processed dataset
        self.final_data = pd.DataFrame({
            'Meal name': ['Pizza', 'Burger', 'Salad', 'Steak'],
            'Restaurant': ['Rest1', 'Rest2', 'Rest1', 'Rest2'],
            'Rating Glovo': [4.5, 3.5, 4.0, 5.0],
            'Price': [10.5, 8.5, 7.0, 12.0]
        })

    def test_simulate_user_ratings(self):
        """
        Test if user ratings simulation produces a DataFrame of correct shape
        and contains expected columns.
        """
        ratings_df = simulate_user_ratings(self.final_data)
        self.assertIsInstance(ratings_df, pd.DataFrame)  # Must be a DataFrame
        self.assertEqual(len(ratings_df.columns), len(self.final_data['Meal name'].unique()))  # Columns match meals
        self.assertGreaterEqual(len(ratings_df), 1000)  # At least 1000 users

    def test_generate_prediction_df(self):
        """
        Test the SVD predictions to ensure the function returns a DataFrame
        and it retains the structure of the user-item matrix.
        """
        user_item_matrix = pd.DataFrame(np.random.rand(10, 4), columns=['Pizza', 'Burger', 'Salad', 'Steak'])
        predictions_df = generate_prediction_df(user_item_matrix)
        self.assertIsInstance(predictions_df, pd.DataFrame)
        self.assertEqual(predictions_df.shape, user_item_matrix.shape)

    @patch('recommendation_system.generate_prediction_df')
    @patch('recommendation_system.simulate_user_ratings')
    def test_recommend_meals(self, mock_simulate, mock_generate):
        """
        Test the recommend_meals function integrates simulation and prediction generation,
        and processes outputs correctly.
        """
        mock_simulate.return_value = pd.DataFrame(np.random.rand(10, 4), columns=['Pizza', 'Burger', 'Salad', 'Steak'])
        mock_generate.return_value = pd.DataFrame(np.random.rand(4, 10), columns=range(1, 11))
        recommendations = recommend_meals(self.final_data)
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertTrue(mock_simulate.called)
        self.assertTrue(mock_generate.called)

if __name__ == '__main__':
    unittest.main()
