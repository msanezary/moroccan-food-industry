import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_distribution(data, column, title):
    plt.figure(figsize=(10, 5))
    sns.histplot(data[column], kde=True)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def plot_correlation(data, column1, column2):
    correlation = data[column1].corr(data[column2])
    sns.jointplot(x=column1, y=column2, data=data, kind='scatter')
    plt.title(f'Correlation: {correlation}')
    plt.show()

def plot_heatmap(data, title):
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    filepath = 'path_to_data.csv'
    data = load_data(filepath)
    plot_distribution(data, 'Rating', 'Distribution of Ratings')
    plot_correlation(data, 'Rating', 'Price')
    plot_heatmap(data, 'Dataset Correlation Heatmap')
