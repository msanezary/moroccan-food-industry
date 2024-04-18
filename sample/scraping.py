#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
from helpers import extract_data
import time 
from geopy.geocoders import Nominatim
import googlemaps
from tqdm import tqdm

def scrape_glovo(city):
    """
    Scrapes Glovo restaurant data for a specified city.

    Parameters:
    city: The city to scrape data for.

    Returns:
    A DataFrame containing all the scraped data from Glovo.
    """
    session = requests.Session()
    url = f'https://glovoapp.com/ma/fr/{city}/restaurants_1/'
    content = session.get(url).text
    soup = BeautifulSoup(content, 'lxml')

    pagination = soup.find('div', class_='category-page__pagination-wrapper')
    nb_pages = int(pagination.find('span', class_='current-page-text').text.split()[-1]) if pagination else 0

    restaurant_links = set()
    for page in tqdm(range(1, nb_pages + 1), desc="Scraping pages"):
        page_url = f'{url}?page={page}'
        page_soup = BeautifulSoup(session.get(page_url).text, 'lxml')
        for link in page_soup.find_all('a', class_='store-card'):
            restaurant_links.add(link['href'])

    df_glovo = pd.DataFrame()
    for link in tqdm(restaurant_links, desc="Processing restaurants"):
        restaurant_url = 'https://glovoapp.com' + link
        restaurant_soup = BeautifulSoup(session.get(restaurant_url).text, 'lxml')
        df_glovo = pd.concat([df_glovo, extract_data(restaurant_soup)], ignore_index=True)

    return df_glovo

def extract_googleMaps(df, city, api_key):
    """
    Extracts Google Maps data for each restaurant in the DataFrame.

    Parameters:
    df: DataFrame containing restaurant data.
    city: City name to append to restaurant names for Google Maps searching.
    api_key: Google Maps API key.

    Returns:
    DataFrame with added Google Maps data including latitude, longitude, and ratings.
    """
    gmaps = googlemaps.Client(key=api_key)
    restaurant_info = pd.DataFrame()
    for restaurant in tqdm(df['Restaurant'].unique(), desc="Fetching Google Maps data"):
        place_name = f"{restaurant} {city}"
        place_result = gmaps.places(place_name)
        if place_result['results']:
            result = place_result['results'][0]
            data = {
                'Restaurant': [restaurant],
                'Address': [result['formatted_address']],
                'Latitude': [result['geometry']['location']['lat']],
                'Longitude': [result['geometry']['location']['lng']],
                'Rating google': [result.get('rating', None)],
                'Number of reviews': [result.get('user_ratings_total', None)],
                'City': [city.upper()]
            }
            restaurant_info = pd.concat([restaurant_info, pd.DataFrame(data)], ignore_index=True)
    return restaurant_info

def extractDistricts(df):
    """
    Adds district information to each restaurant using geopy.

    Parameters:
    df: DataFrame containing restaurant data with latitude and longitude.

    Returns:
    DataFrame with district information added.
    """
    geolocator = Nominatim(user_agent="my_app")
    tqdm.pandas(desc="Extracting Districts")  # Initialize tqdm for pandas apply
    
    # Use progress_apply instead of apply to integrate tqdm for visual progress
    df['District'] = df.progress_apply(lambda row: geolocator.reverse((row['Latitude'], row['Longitude'])).raw.get('address', {}).get('city_district', None), axis=1) ##Sometimes, city_district can be called municipality, district... So you should check the address list before
    return df
