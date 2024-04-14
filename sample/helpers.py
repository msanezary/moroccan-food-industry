#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd  # Ensure pandas is imported for DataFrame operations.

def concat_liste(liste, sep):
    """
    Concatenates the strings in a list of lists with a separator.
    
    Parameters:
    liste: A list of lists of strings.
    sep: The separator string (could be space, underscore, etc.).

    Returns:
    A list of concatenated strings.
    """
    return [sep.join(l) for l in liste]

def extract(liste_html, sep):
    """
    Extracts text from HTML tags and concatenates the strings with a separator.
    This function avoids multiple BeautifulSoup searches by reusing extracted results.

    Parameters:
    liste_html: A list of BeautifulSoup tag objects.
    sep: The separator string.

    Returns:
    A list of concatenated strings.
    """
    return concat_liste([l.text.split() for l in liste_html], sep)

def extract_data(soup):
    """
    Extracts data from a restaurant's link parsed by BeautifulSoup.

    Parameters:
    soup : The BeautifulSoup object parsed from the restaurant's link HTML content.

    Returns:
    A pandas DataFrame containing restaurant's data.
    """
    try:
        local_df = pd.DataFrame(columns=['Restaurant', 'Link to Glovo', 'Meal category', 'Meal name', 'Ingredients', 'Price', 'Rating Glovo'])
        dish_categories = soup.find_all('div', class_='store__body__dynamic-content')
        ratings = soup.find_all('span', class_='store-rating__label')
        store_names = soup.find_all('h1', class_='store-info__title')

        rating = extract(ratings, ' ')
        store = [extract(store_names, ' ')[0]] if store_names else [None]

        for dish_category in dish_categories:
            dishes = dish_category.find_all('div', class_='list')
            for dish in dishes:
                dish_type = dish.find('p', class_='list__title')
                products = dish.find_all('div', class_='product-row__name')
                ingredients = [extract([ingredient], ' ')[0] if ingredient else np.nan 
                               for ingredient in dish.find_all('div', class_='product-row__info')]
                prices = extract(dish.find_all('span', class_='product-price__effective product-price__effective--new-card'), ' ')
                dish_type_text = extract([dish_type], ' ') if dish_type else [None]

                data = {
                    'Restaurant': store * len(products),
                    'Link to Glovo': ['link_placeholder'] * len(products),
                    'Dish category': dish_type_text * len(products),
                    'Dish name': extract(products, ' '),
                    'Ingredients': ingredients,
                    'Price': prices,
                    'Rating Glovo': rating * len(products)
                }
                local_df = pd.concat([local_df, pd.DataFrame(data)], ignore_index=True)
        return local_df
    except Exception as e:
        print(f"Error processing HTML content: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error.

def clean_price(price):
    """
    Converts the price from a string to a float, removing the Moroccan currency 'MAD'.

    Parameters:
    price : A string that contains the price.

    Returns:
    The price as a float or NaN if conversion fails.
    """
    try:
        return '{:.2f}'.format(float(price.replace(' ','').split('MAD')[0].replace(',','.')))
    except ValueError:
        return np.nan

def clean_percentage(rating):
    """
    Converts the rating from a percentage string to an integer, removing the '%' sign.

    Parameters:
    rating : A string representing the rating.

    Returns:
    The rating as an integer or NaN if conversion fails.
    """
    try:
        return int(rating.replace('%', '')) if '%' in rating else int(rating)
    except ValueError:
        return np.nan
