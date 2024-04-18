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
        self.data = pd.DataFrame({
            'Price': ['100 MAD', '200 MAD'],
            'Rating Glovo': ['80%', '--'],
            'Meal name': ['Pizza', 'Burger']
        })

    def test_preprocess_data(self):
        processed_data = preprocess_data(self.data)
        self.assertFalse(processed_data.empty)
        self.assertNotIn('--', processed_data['Rating Glovo'])

    def test_classify_meals(self):
        # Mock the necessary files and inputs for the classification
        processed_data = preprocess_data(self.data)
        classified_data = classify_meals(processed_data, 'path_to_categories.csv')
        self.assertIn('Category', classified_data.columns)

if __name__ == '__main__':
    unittest.main()
