import unittest
import sys
import os
from unittest.mock import patch
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Append the directory of your helpers module to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample')))
from helpers import concat_liste, extract, extract_data, clean_price, clean_percentage

class TestHelpers(unittest.TestCase):

    def test_concat_liste(self):
        self.assertEqual(concat_liste([['hello', 'world'], ['test']], ' '), ['hello world', 'test'])

    def test_extract(self):
        html = "<div>Hello World</div>"
        soup = BeautifulSoup(html, 'html.parser')
        self.assertEqual(extract([soup.div], ' '), ['Hello World'])

    def test_extract_data(self):
        html = "<div class='store__body__dynamic-content'></div>"
        soup = BeautifulSoup(html, 'html.parser')
        df = extract_data(soup)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_clean_price(self):
        self.assertEqual(clean_price(" 123,45 MAD "), 123.45)
        self.assertTrue(np.isnan(clean_price("invalid")))

    def test_clean_percentage(self):
        self.assertEqual(clean_percentage("85%"), 85)
        self.assertTrue(np.isnan(clean_percentage("invalid")))

if __name__ == '__main__':
    unittest.main()
