"""Save Trained Model Artifacts
Trains and serializes the best performing Gradient Boosting model and
the ColumnTransformer preprocessor for real-time inference in the Streamlit app.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

def train_and_export():
    df = pd.read_csv("data/processed/flipkart_cleaned.csv")
    
    num_features = [
        "retail_price",
        "product_name_word_count",
        "description_word_count",
        "is_FK_Advantage_product",
        "is_rated"
    ]
    cat_features = ["primary_category", "brand"]
    
    X = df[num_features + cat_features].copy()
    y = df["discounted_price"].values
    
    X["primary_category"] = X["primary_category"].fillna("Unknown").astype(str)
    X["brand"] = X["brand"].fillna("Unbranded / Generic").astype(str)
    X["is_FK_Advantage_product"] = X["is_FK_Advantage_product"].astype(int)
    X["is_rated"] = X["is_rated"].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30, sparse_output=False), cat_features)
        ],
        remainder="drop"
    )
    
    X_train_proc = preprocessor.fit_transform(X_train)
    
    gb_model = GradientBoostingRegressor(
        n_estimators=120,
        learning_rate=0.08,
        max_depth=6,
        random_state=42
    )
    gb_model.fit(X_train_proc, y_train)
    
    top_categories = sorted(df["primary_category"].value_counts().head(25).index.tolist())
    top_brands = sorted(df[df["brand"] != "Unbranded / Generic"]["brand"].value_counts().head(30).index.tolist())
    
    artifacts = {
        "model": gb_model,
        "preprocessor": preprocessor,
        "num_features": num_features,
        "cat_features": cat_features,
        "top_categories": top_categories,
        "top_brands": top_brands
    }
    
    out_file = Path("models/saved/price_model_artifacts.joblib")
    joblib.dump(artifacts, out_file)
    print(f"Successfully serialized model artifacts to: {out_file}")

if __name__ == "__main__":
    train_and_export()
