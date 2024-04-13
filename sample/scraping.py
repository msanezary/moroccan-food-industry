#!/usr/bin/env python
# coding: utf-8

"""
Scraping module for the 'Tasting Data' project: Exploring Morocco's Food Industry
and Making Some Recommendations
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def concat_list(list_of_lists, separator):
    """Concatenates the strings in a list of lists with a separator."""
    return [separator.join(items) for items in list_of_lists]

def extract_text(html_list, separator):
    """Extracts text from a list of BeautifulSoup tag objects and concatenates them with a separator."""
    return concat_list([tag.text.split() for tag in html_list], separator)

def extract_data(soup):
    """Extracts data from a restaurant's webpage and returns it as a pandas DataFrame."""
    local_df = pd.DataFrame(columns=['Restaurant', 'Link to glovo', 'Dish category', 'Dish name', 'Ingredients', 'Price', 'Rating glovo'])
    dish_categories = soup.find_all('div', class_='store__body__dynamic-content')
    ratings = soup.find_all('span', class_='store-rating__label')
    store_name = soup.find_all('h1', class_='store-info__title')
    
    # Process text extraction
    rating = extract_text(ratings, ' ')
    store = [extract_text(store_name, ' ')[0]] if store_name else [None]

    # Iterate through each category and dish
    for category in dish_categories:
        dishes = category.find_all('div', class_='list')
        for dish in dishes:
            dish_type = dish.find('p', class_='list__title')
            products = dish.find_all('div', class_='product-row__name')
            ingredients = extract_ingredients(dish)
            prices = extract_prices(dish)
            dish_type_text = extract_text([dish_type], ' ') if dish_type else None

            # Prepare data for DataFrame
            data = {
                'Restaurant': store * len(products),
                'Link to glovo': ['link_placeholder'] * len(products),
                'Dish category': dish_type_text * len(products),
                'Dish name': extract_text(products, ' '),
                'Ingredients': ingredients,
                'Price': prices,
                'Rating glovo': rating * len(products)
            }
            local_df = pd.concat([local_df, pd.DataFrame(data)], ignore_index=True)
            
    return local_df

def extract_ingredients(dish):
    """Extracts ingredients from a dish listing."""
    ingredients = []
    for product in dish.find_all('div', class_='product-row__info'):
        ingredient = product.find_all('span', class_='product-row__info__description')
        ingredients.append(extract_text(ingredient, ' ')[0] if ingredient else None)
    return ingredients

def extract_prices(dish):
    """Extracts prices from a dish listing."""
    prices = dish.find_all('span', class_='product-price__effective product-price__effective--new-card')
    return extract_text(prices, ' ')

def scrape_glovo(city):
    """Scrapes Glovo restaurant data for a specified city."""
    session = requests.Session()
    base_url = f'https://glovoapp.com/ma/fr/{city}/restaurants_1/'
    content = session.get(base_url).text
    soup = BeautifulSoup(content, 'lxml')

    # Find number of pages
    pagination = soup.find('div', class_='category-page__pagination-wrapper')
    if pagination:
        nb_pages = int(pagination.find('span', class_='current-page-text').text.split()[-1])

        # Collect links from all pages
        restaurant_links = set()
        for page in range(1, nb_pages + 1):
            page_url = f'{base_url}?page={page}'
            response = session.get(page_url)
            page_soup = BeautifulSoup(response.content, 'lxml')
            restaurants = page_soup.find_all('a', class_='collection-item hover-effect full-width--mobile')
            for restaurant in restaurants:
                restaurant_links.add(restaurant['href'])

        # Scrape data from each restaurant link
        full_data = pd.DataFrame()
        for link in restaurant_links:
            restaurant_url = 'https://glovoapp.com' + link
            restaurant_content = session.get(restaurant_url).text
            restaurant_soup = BeautifulSoup(restaurant_content, 'lxml')
            restaurant_data = extract_data(restaurant_soup)
            full_data = pd.concat([full_data, restaurant_data], ignore_index=True)

        return full_data
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no pagination found
