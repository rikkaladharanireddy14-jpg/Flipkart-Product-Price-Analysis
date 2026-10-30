"""Feature Engineering Module
Creates validated analytical features, price tiers, and transformations.

CRITICAL DATA LEAKAGE RULE:
If training a model to predict `discounted_price`, NEVER use `discount_percentage`
or `discount_amount` as input features, because they are mathematically computed
using the target variable:
    discount_percentage = ((retail_price - discounted_price) / retail_price) * 100
"""

import numpy as np
import pandas as pd
from typing import Tuple


def add_pricing_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes discount amounts, percentages, tiers, and log-transformed prices.
    
    Args:
        df: Cleaned Flipkart DataFrame.
        
    Returns:
        pd.DataFrame with added analytical features.
    """
    df = df.copy()
    
    # 1. Discount amount and percentage
    df["discount_amount"] = (df["retail_price"] - df["discounted_price"]).clip(lower=0.0)
    df["discount_percentage"] = (
        (df["discount_amount"] / df["retail_price"]) * 100.0
    ).round(2).clip(lower=0.0, upper=100.0)
    
    # 2. Discount Tiers
    discount_bins = [-1.0, 0.0, 25.0, 50.0, 75.0, 100.0]
    discount_labels = [
        "No Discount (0%)",
        "Low Discount (1-25%)",
        "Moderate Discount (26-50%)",
        "High Discount (51-75%)",
        "Clearance (>75%)"
    ]
    df["discount_tier"] = pd.cut(
        df["discount_percentage"],
        bins=discount_bins,
        labels=discount_labels,
        right=True
    )
    
    # 3. Retail Price Tiers (INR)
    price_bins = [0.0, 500.0, 1500.0, 5000.0, 15000.0, np.inf]
    price_labels = [
        "Budget (< ₹500)",
        "Economy (₹500 - ₹1,500)",
        "Mid-Range (₹1,500 - ₹5,000)",
        "Premium (₹5,000 - ₹15,000)",
        "Luxury (> ₹15,000)"
    ]
    df["price_tier"] = pd.cut(
        df["retail_price"],
        bins=price_bins,
        labels=price_labels,
        right=False
    )
    
    # 4. Log transformations for heavy right-skew handling
    df["log_retail_price"] = np.log1p(df["retail_price"]).round(4)
    df["log_discounted_price"] = np.log1p(df["discounted_price"]).round(4)
    
    # 5. Text Length Metadata
    df["product_name_char_count"] = df["product_name"].astype(str).str.len()
    df["product_name_word_count"] = df["product_name"].astype(str).str.split().str.len()
    
    desc_str = df["description"].fillna("").astype(str)
    df["description_char_count"] = desc_str.str.len()
    df["description_word_count"] = desc_str.str.split().str.len()
    
    return df


def get_modeling_features_and_target(
    df: pd.DataFrame,
    target_type: str = "discounted_price"
) -> Tuple[pd.DataFrame, pd.Series]:
    """Extracts features and target preventing data leakage.
    
    Args:
        df: Feature-engineered DataFrame.
        target_type: 'discounted_price' or 'discount_percentage'.
        
    Returns:
        Tuple[X, y]: Feature matrix (guaranteed free of leakage) and target series.
    """
    if target_type == "discounted_price":
        # Target is discounted_price
        # EXCLUDE discount_percentage, discount_amount, discount_tier, log_discounted_price!
        leakage_cols = [
            "discounted_price",
            "log_discounted_price",
            "discount_amount",
            "discount_percentage",
            "discount_tier"
        ]
        y = df["discounted_price"]
    elif target_type == "discount_percentage":
        # Target is discount_percentage
        # EXCLUDE discounted_price, discount_amount, discount_tier!
        leakage_cols = [
            "discount_percentage",
            "discount_tier",
            "discount_amount",
            "discounted_price",
            "log_discounted_price"
        ]
        y = df["discount_percentage"]
    else:
        raise ValueError(f"Unsupported target_type: {target_type}")
        
    # Standard candidate feature columns
    candidate_features = [
        "retail_price",
        "log_retail_price",
        "price_tier",
        "primary_category",
        "sub_category",
        "brand",
        "is_FK_Advantage_product",
        "product_name_char_count",
        "product_name_word_count",
        "description_char_count",
        "description_word_count",
        "is_rated",
        "rating_score"
    ]
    
    # Ensure no leakage columns are present in features
    clean_features = [c for c in candidate_features if c not in leakage_cols]
    X = df[clean_features].copy()
    
    return X, y
