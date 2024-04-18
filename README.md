# Tasting Data: Exploring Morocco's Food Industry

## Introduction
Welcome to "Moroccan Food Industry", a project aimed at exploring Morocco's food industry by extracting and analyzing data from Moroccan restaurants. Our ultimate goal is to uncover insights into dining trends and consumer preferences, which will aid in developing a recommendation system tailored to customer preferences.

### Project Author
Mohammed Said ANEZARY

**LinkedIn Profile:** [Mohammed Said ANEZARY](https://www.linkedin.com/in/msanezary/)\\
**Email:** [email](msanezary@gmail.com)

## Project Objective
This project seeks to leverage data to understand the dynamics of the Moroccan food market and to provide actionable insights through a recommendation system. Specifically, we aim to:
- Analyze data from various Moroccan restaurants.
- Understand consumer dining preferences and trends.
- Develop a system that recommends restaurants based on user preferences.

## Key Features
- **Data Extraction**: Utilize BeautifulSoup for web scraping data from Glovo's Moroccan site.
- **Geographical Insights**: Leverage the Google Maps API for acquiring geographical data and customer ratings.
- **District Classification**: Utilize the "geopy" library to categorize restaurants into districts based on their location.
- **Machine Learning Modeling**: Implement machine learning to predict dish types and develop a recommendation system.
- **Collaborative Filtering**: Build a Collaborative Based Recommendation System to suggest dining options to users.

## Technologies Used
- Python
- Libraries: BeautifulSoup, pandas, numpy, requests, googlemaps, geopy, sklearn
- APIs: Google Maps

## Remarks:
* Since this project relies on the HTML code structure of the Glovo Moroccan website, some modifications may be necessary for it to work properly in your country.
* The googlemaps Places API can be obtained from [Developer google Places API](https://console.cloud.google.com/apis/library/places-backend.googleapis.com?hl=fr&project=prefab-phoenix-384223)

## Setup and Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/msanezary/moroccan-food-industry.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd moroccan-food-industry
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Use
To run the project and view the analysis:
1. Execute the main script:
   ```bash
   python sample/core.py
   ```

## Data
Data is scraped from the Glovo website, specifically targeting Moroccan restaurants. The data includes restaurant names, dish types, prices, customer ratings, and geographical coordinates.

## Contribution
Contributions are welcome! Please feel free to fork this repository, make your changes, and submit a pull request.

## Licensing
This project is released under the MIT License. For more details, see the [LICENSE](LICENSE) file included with this repository.

## Data Analysis
For a detailed exploration of the data and insights, see our [Data Analysis Notebook](notebook\Tasting data-Morocco.ipynb).

The notebook includes detailed data cleaning, exploratory data analysis, visualizations of key trends, and the application of machine learning models for predictions. It provides insights into the dining preferences and trends observed across various districts in Morocco.

### Running the Notebook
- **Locally**: Ensure you have Jupyter installed (`pip install notebook`). Navigate to the project directory and run `jupyter notebook`.
- **Google Colab**: You can also view and run the notebook in [Google Colab](https://colab.research.google.com) by uploading the notebook file there.
-[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/msanezary/moroccan-food-industry/main?filepath=notebook%2Fdata_analysis.ipynb)


## Acknowledgments
- Thanks to Glovo for providing the dataset used in the analysis.
- Appreciation to Google Maps and geopy for geolocation tools.
- Gratitude for the open-source tools and libraries like Jupyter, Pandas, and Matplotlib that made this analysis possible.
