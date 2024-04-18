#!/usr/bin/env python
# coding: utf-8

import logging
import os
import sys
from argparse import ArgumentParser
from scraping import scrape_glovo, extract_googleMaps, extractDistricts
from data_preprocessing import preprocess_data, classify_meals, save_final_dataset
from recommendation_system import generate_user_item_matrix, generate_prediction_df, recommend_meals

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    parser = ArgumentParser(description="Run the food industry data processing pipeline.")
    parser.add_argument('--city', default='tanger', help='City to process data for.')
    parser.add_argument('--api_key', default=os.getenv('GOOGLE_MAPS_API_KEY', 'Your_key'), help='Google Maps API key.')
    parser.add_argument('--output_dir', default=os.path.join(base_dir, '..', 'results'), help='Directory to save output files.')
    return parser.parse_args()

def main():
    base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    args = parse_args()
    setup_logging()

    if args.api_key == 'Your_Google_Maps_API_Key':
        logging.error("Google Maps API key not provided.")
        sys.exit(1)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    try:
        logging.info("Starting data collection...")
        df_glovo = scrape_glovo(args.city)
        df_maps = extract_googleMaps(df_glovo, args.city, args.api_key)
        df_complete = extractDistricts(df_maps)

        logging.info("Preprocessing data...")
        processed_data = preprocess_data(df_complete)

        logging.info("Classifying meals...")
        final_data = classify_meals(processed_data, os.path.join(base_dir, '..', 'datasets', 'categories.csv'))

        final_data_path = os.path.join(args.output_dir, 'final_dataset.csv')
        save_final_dataset(final_data, final_data_path)
        logging.info(f"Final dataset saved at {final_data_path}")


        processed_data = preprocess_data(df_complete)
        final_data = classify_meals(processed_data, os.path.join(base_dir, '..', 'datasets', 'categories.csv'))

        logging.info("Genrating the recommendation system...")
        predictions = recommend_meals(final_data)
        predictions_path = os.path.join(args.output_dir, 'predictions.csv')
        predictions.to_csv(predictions_path)
        logging.info(f"Recommendations saved at {predictions_path}")


    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
