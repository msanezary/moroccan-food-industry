#!/usr/bin/env python
# coding: utf-8

"""
Analysis module for the 'Tasting Data' project: Analyzing Morocco's Food Industry.
"""

import pandas as pd

def compute_average_ratings(df, rating_column='Rating'):
    """Compute the average rating for each restaurant."""
    return df.groupby('Restaurant')[rating_column].mean()

def compute_rating_correlations(df, rating_column='Rating', review_column='Number of Reviews'):
    """Compute the correlation between ratings and number of reviews."""
    correlation = df[rating_column].corr(df[review_column])
    return correlation

def top_categories_by_count(df, category_column='Category', top_n=10):
    """Return the top N food categories by count."""
    return df[category_column].value_counts().head(top_n)

# Example usage
if __name__ == '__main__':
    data = pd.read_csv('path_to_data.csv')
    
    # Calculate average ratings
    averages = compute_average_ratings(data)
    print("Average Ratings:\n", averages)
    
    # Calculate correlation between ratings and number of reviews
    correlation = compute_rating_correlations(data)
    print("Correlation between ratings and number of reviews: ", correlation)
    
    # Get top food categories
    top_categories = top_categories_by_count(data)
    print("Top Food Categories:\n", top_categories)
