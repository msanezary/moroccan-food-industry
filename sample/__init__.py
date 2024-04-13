# __init__.py
from .scraping import fetch_restaurant_data
from .analysis import perform_analysis
from .visualization import create_visualizations
from .recommendation_system import setup_recommendation_system

__all__ = [
    'fetch_restaurant_data',
    'perform_analysis',
    'create_visualizations',
    'setup_recommendation_system'
]
