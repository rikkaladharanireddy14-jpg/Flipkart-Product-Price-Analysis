"""Data Cleaning Module
Performs robust, validated cleaning on the raw Flipkart dataset without
altering or overwriting the raw data file.
"""

import re
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


def parse_category_tree(category_str: Any) -> Tuple[str, str, str]:
    """Parses Flipkart nested category tree string into discrete hierarchy levels.
    
    Example input:
        '["Clothing >> Women\'s Clothing >> Lingerie, Sleep & Swimwear >> Shorts"]'
        
    Returns:
        Tuple[str, str, str]: (primary_category, sub_category, micro_category)
    """
    if not isinstance(category_str, str) or not category_str.strip():
        return ("Unknown", "Unknown", "Unknown")
    
    # Strip brackets, quotes, and whitespace
    cleaned = category_str.strip("[]\"' \t\r\n")
    parts = [p.strip().strip("\"'") for p in cleaned.split(">>") if p.strip()]
    
    primary = parts[0] if len(parts) > 0 and parts[0] else "Unknown"
    sub = parts[1] if len(parts) > 1 and parts[1] else "Unknown"
    micro = parts[2] if len(parts) > 2 and parts[2] else "Unknown"
    
    return (primary, sub, micro)


def clean_flipkart_data(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Cleans the raw dataset applying strictly validated domain rules.
    
    Rules applied:
    1. Retain raw immutability by operating on a deep copy.
    2. Drop records where retail_price or discounted_price is NaN or <= 0 (78 rows = 0.39%).
    3. Retain legitimate product variants: do NOT drop rows solely based on repeated product_name.
    4. Handle rating transparency: convert 'No rating available' to NaN and add 'is_rated' flag.
    5. Clean brand names: preserve missing brands as 'Unbranded / Generic' without guessing.
    6. Parse product_category_tree into primary_category, sub_category, and micro_category.
    7. Convert crawl_timestamp to ISO datetime.
    
    Args:
        df_raw: Original raw DataFrame.
        
    Returns:
        Tuple[pd.DataFrame, Dict[str, Any]]: Cleaned DataFrame and audit report dict.
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 1. Deduplicate by unique listing identifier (uniq_id)
    df = df.drop_duplicates(subset=["uniq_id"]).reset_index(drop=True)
    dedup_rows = len(df)
    
    # 2. Clean and convert prices
    df["retail_price"] = pd.to_numeric(df["retail_price"], errors="coerce")
    df["discounted_price"] = pd.to_numeric(df["discounted_price"], errors="coerce")
    
    # Drop records with invalid or missing prices
    valid_price_mask = (
        df["retail_price"].notna() &
        df["discounted_price"].notna() &
        (df["retail_price"] > 0) &
        (df["discounted_price"] > 0)
    )
    dropped_prices = int((~valid_price_mask).sum())
    df = df[valid_price_mask].copy().reset_index(drop=True)
    
    # 3. Category Tree Extraction
    category_parsed = df["product_category_tree"].apply(parse_category_tree)
    df["primary_category"] = [cat[0] for cat in category_parsed]
    df["sub_category"] = [cat[1] for cat in category_parsed]
    df["micro_category"] = [cat[2] for cat in category_parsed]
    
    # 4. Brand Cleaning - Strict adherence: do NOT impute from product_name
    df["brand"] = df["brand"].astype(str).str.strip()
    df["brand"] = df["brand"].replace({
        "": "Unbranded / Generic",
        "nan": "Unbranded / Generic",
        "None": "Unbranded / Generic",
        "null": "Unbranded / Generic"
    })
    
    # 5. Rating Cleaning & Documentation
    # Replace non-numerical placeholder with NaN
    df["product_rating"] = df["product_rating"].astype(str).str.strip()
    rating_clean = pd.to_numeric(
        df["product_rating"].replace("No rating available", np.nan),
        errors="coerce"
    )
    df["rating_score"] = rating_clean
    df["is_rated"] = df["rating_score"].notna().astype(int)
    
    # 6. Flipkart Advantage Boolean
    df["is_FK_Advantage_product"] = df["is_FK_Advantage_product"].astype(str).str.lower() == "true"
    
    # 7. Timestamp conversion
    df["crawl_datetime"] = pd.to_datetime(df["crawl_timestamp"], errors="coerce")
    
    final_rows = len(df)
    rated_count = int(df["is_rated"].sum())
    
    stats = {
        "initial_rows": initial_rows,
        "after_dedup_rows": dedup_rows,
        "dropped_invalid_price_rows": dropped_prices,
        "final_clean_rows": final_rows,
        "final_clean_columns": df.shape[1],
        "rated_products_count": rated_count,
        "unrated_products_count": final_rows - rated_count,
        "rated_percentage": round((rated_count / final_rows) * 100, 2),
        "unbranded_products_count": int((df["brand"] == "Unbranded / Generic").sum()),
        "distinct_primary_categories": int(df["primary_category"].nunique()),
        "distinct_brands": int(df["brand"].nunique()),
    }
    
    return df, stats
