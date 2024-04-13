import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def load_data(filepath):
    return pd.read_csv(filepath)

def setup_pipeline():
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression())
    ])
    return pipeline

def train_model(data, feature_col, target_col):
    X_train, X_test, y_train, y_test = train_test_split(data[feature_col], data[target_col], test_size=0.2, random_state=42)
    pipeline = setup_pipeline()
    pipeline.fit(X_train, y_train)
    return pipeline, X_test, y_test

def evaluate_model(pipeline, X_test, y_test):
    predictions = pipeline.predict(X_test)
    report = classification_report(y_test, predictions)
    print(report)

if __name__ == "__main__":
    filepath = 'path_to_dish_data.csv'
    data = load_data(filepath)
    model, X_test, y_test = train_model(data, 'Dish name', 'Type')
    evaluate_model(model, X_test, y_test)
