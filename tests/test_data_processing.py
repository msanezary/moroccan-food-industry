import unittest
import sys
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Append the directory of your helpers module to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample')))

from data_preprocessing import preprocess_data, classify_meals

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        """Set up test data and expected results."""
        self.data = pd.DataFrame({
        'Restaurant': ['R1', 'R2', 'R3', 'R4', 'R5'],
        'Meal name': ['M1', 'M2', 'M3', 'M4', 'M5'],
        'Price': ['100 MAD', '200 USD', '300 USD', '400 MAD', '--'],
        'Rating glovo': ['80%', '--', '70%', '90%', '100%'],
        'Rating google': [4.0, np.nan, 3.5, 4.5, 5.0],
        'Latitude': [34.05, 34.05, np.nan, 34.05, 34.05],
        'Longitude': [-6.80, -6.80, -6.80, np.nan, -6.80]
    })

    def test_non_empty_output(self):
        """Test that the function returns a non-empty DataFrame when given valid input."""
        processed_data = preprocess_data(self.data)
        self.assertFalse(processed_data.empty)

    def test_ignore_non_mad_prices(self):
        """Test that rows without 'MAD' in the price are ignored."""
        processed_data = preprocess_data(self.data)
        self.assertEqual(len(processed_data), 2)  # Only two entries should remain

    def test_correct_rating_calculation(self):
        """Test the correct calculation of composite ratings."""
        processed_data = preprocess_data(self.data)
        expected_ratings = [4.0, (4.5 + 0.9) / 2, 5.0]  # Based on given data and function logic
        calculated_ratings = list(processed_data['Rating'])
        np.testing.assert_array_almost_equal(expected_ratings, calculated_ratings)

    def test_handling_invalid_data(self):
        """Test the function's ability to handle and skip over invalid data."""
        invalid_data = pd.DataFrame({
            'Restaurant': ['Invalid'],
            'Meal name': ['InvalidMeal'],
            'Price': ['Not a price'],
            'Rating glovo': ['Not a percentage'],
            'Rating google': ['Not a rating'],
            'Latitude': [None],
            'Longitude': [None]
        })
        processed_data = preprocess_data(invalid_data)
        self.assertTrue(processed_data.empty)

    def test_drop_missing_coordinates(self):
        """Ensure rows with missing latitude or longitude are dropped."""
        processed_data = preprocess_data(self.data)
        self.assertNotIn('R3', processed_data['Restaurant'].values)
        self.assertNotIn('R4', processed_data['Restaurant'].values)

    def test_classify_meals(self):
        # Mock the necessary files and inputs for the classification
        processed_data = preprocess_data(self.data)
        classified_data = classify_meals(processed_data, 'path_to_categories.csv')
        self.assertIn('Category', classified_data.columns)

if __name__ == '__main__':
    unittest.main()
