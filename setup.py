from setuptools import setup, find_packages

setup(
    name='TastingData',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/msanezary/moroccan-food-industry',
    license='MIT',
    author='Mohammed Said ANEZARY',
    author_email='msanezary@gmail.com',
    description='Exploring Morocco\'s Food Industry and Making Recommendations',
    install_requires=[
        'numpy',
        'pandas',
        'beautifulsoup4',
        'requests',
        'googlemaps',
        'geopy',
        'matplotlib',
        'seaborn',
        'plotly',
        'folium',
        'scikit-learn',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='food industry analysis morocco restaurants machine learning',  # Keywords that define your package best
)
