#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from helpers import clean_price, clean_percentage


def preprocess_data(final_data):
    """
    Cleans and preprocesses the given DataFrame by converting currency, handling missing data, 
    and creating a composite rating.

    Parameters:
    final_data (DataFrame): The dataset containing restaurant information.

    Returns:
    DataFrame: The preprocessed data.
    """
    print("Initial data count:", len(final_data))

    # Clean price data: only keep rows with 'MAD' in 'Price'
    final_data['Price'] = final_data['Price'].apply(clean_price)
    final_data = final_data.dropna(subset=['Price'])
    print("After MAD filter and price conversion:", len(final_data))

    if final_data.empty:
        return final_data

    # Replace '--' with NaN in the entire DataFrame
    final_data = final_data.replace('--', np.nan)

    # Clean ratings data: Correct column name to 'Rating glovo'
    final_data['Rating glovo'] = final_data['Rating glovo'].apply(clean_percentage)

    # Create a composite rating
    df_rating = pd.DataFrame(columns=['Meal name', 'Rating'])
    for i in range(len(final_data)):
        glovo_rating = final_data.iloc[i]['Rating glovo']
        google_rating = final_data.iloc[i].get('Rating google', np.nan)
        if np.isnan(glovo_rating):
            rating = google_rating
        elif np.isnan(google_rating):
            rating = glovo_rating
        else:
            rating = (glovo_rating + google_rating) / 2
        df_rating = pd.concat([df_rating, pd.DataFrame({'Meal name': [final_data.iloc[i]['Meal name']], 'Rating': [rating]})], ignore_index=True)
    
    print("Ratings calculated:", len(df_rating))

    final_data = pd.merge(final_data, df_rating, on='Meal name', how='left')
    print("After merging with ratings:", len(final_data))

    # Drop columns 'Rating glovo', 'Rating google'
    final_data = final_data.drop(columns=['Rating glovo', 'Rating google'], errors='ignore')

    # Remove duplicate entries based on 'Restaurant' and 'Meal name'
    final_data = final_data.drop_duplicates(subset=['Restaurant', 'Meal name'], keep='last')
    print("After dropping duplicates:", len(final_data))

    # Drop rows missing 'Latitude' or 'Longitude'
    final_data.dropna(axis='index', subset=['Latitude', 'Longitude'], inplace=True)
    print("After dropping rows with missing coordinates:", len(final_data))

    final_data = final_data.reset_index(drop=True)
    
    return final_data


def classify_meals(final_data, categories_file_path):
    """
    Classifies meals based on the provided training data.

    Parameters:
    final_data (DataFrame): The dataset to classify.
    categories_file_path (str): Path to the CSV file containing the training data.

    Returns:
    DataFrame: The classified data.
    """
    try:
        # Load training data
        meal_category = pd.read_csv(categories_file_path, encoding='utf-8', sep=';')
        categories = meal_category['Type']
        meals = meal_category['Plat']

        # Prepare the data
        X_train, X_test, y_train, y_test = train_test_split(meals, categories, test_size=0.2, random_state=42)
        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Train classifier
        classifier = RandomForestClassifier()
        classifier.fit(X_train_vec, y_train)
        accuracy = accuracy_score(y_test, classifier.predict(X_test_vec))

        # Train the final classifier
        X_vect = vectorizer.fit_transform(meals)
        classifier = LogisticRegression()
        classifier.fit(X_vect, categories)

        # Predict the categories for final_data
        df_categories = pd.DataFrame(columns=['Meal name', 'Category'])
        for i in range(len(final_data)):
            meal_name = final_data.loc[i]['Meal name']
            category = classifier.predict(vectorizer.transform([meal_name]))
            df_categories = pd.concat([df_categories, pd.DataFrame({'Meal name': [meal_name], 'Category': category[0]})], ignore_index=True)

        final_data = pd.merge(final_data, df_categories, on='Meal name')
        final_data = final_data.drop_duplicates(subset=['Restaurant', 'Meal name'], keep='last')
        final_data = final_data.reset_index(drop=True)

        return final_data
    except Exception as e:
        print(f"Error in classifying meals: {e}")
        return pd.DataFrame()

def save_final_dataset(final_data, output_path):
    """
    Saves the final dataset to a CSV file.

    Parameters:
    final_data (DataFrame): The dataset to save.
    output_path (str): The file path where the dataset should be saved.
    """
    try:
        final_data.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Failed to save data: {e}")
