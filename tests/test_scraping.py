import unittest
import sys
import os
from unittest.mock import patch
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Append the directory of your helpers module to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample')))
from scraping import scrape_glovo, extract_googleMaps

class TestScraping(unittest.TestCase):

    @patch('scraping.requests.Session.get')
    def test_scrape_glovo(self, mock_get):
        mock_get.return_value.text = '<div class="store-card"></div>'
        df = scrape_glovo('test_city')
        self.assertTrue(isinstance(df, pd.DataFrame))

    @patch('scraping.googlemaps.Client')
    def test_extract_googleMaps(self, mock_client):
        # Setup the mock client and its return values
        mock_places = mock_client.return_value.places
        mock_places.return_value = {'results': [{'formatted_address': '123 Test St', 'geometry': {'location': {'lat': 10, 'lng': 20}}, 'rating': 4.5, 'user_ratings_total': 50}]}

        df = pd.DataFrame({'Restaurant': ['Test Restaurant'], 'Latitude': [10], 'Longitude': [20]})
        df = extract_googleMaps(df, 'Test City', 'fake_api_key')

        self.assertIsNotNone(df)
        self.assertEqual(df.iloc[0]['Address'], '123 Test St')

if __name__ == '__main__':
    unittest.main()
