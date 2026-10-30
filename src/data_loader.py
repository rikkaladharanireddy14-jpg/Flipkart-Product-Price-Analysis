"""Data Loader Module
Loads raw and processed Flipkart datasets, runs initial schema checks,
and audits duplicate identifiers (uniq_id and pid separately).
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd


def load_raw_data(filepath: str = "data/raw/flipkart_com-ecommerce_sample.csv") -> pd.DataFrame:
    """Loads the original raw Flipkart dataset in read-only fashion.
    
    Args:
        filepath: Relative or absolute path to raw CSV.
        
    Returns:
        pd.DataFrame: Original unchanged raw DataFrame.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at: {filepath}")
    
    # Read raw data with explicit encoding
    df = pd.read_csv(path, encoding="utf-8")
    return df


def audit_identifiers(df: pd.DataFrame) -> Dict[str, Any]:
    """Audits uniq_id, pid, and product_name uniqueness separately.
    
    Products are NOT removed solely because their product names repeat,
    as multiple sellers or product variants (color/size) legitimately share titles.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Dict summarizing distinct counts and duplicate records.
    """
    total_records = len(df)
    uniq_id_count = df["uniq_id"].nunique()
    pid_count = df["pid"].nunique()
    product_name_count = df["product_name"].nunique()

    dup_uniq_ids = df[df.duplicated(subset=["uniq_id"], keep=False)]
    dup_pids = df[df.duplicated(subset=["pid"], keep=False)]

    return {
        "total_records": total_records,
        "distinct_uniq_id": uniq_id_count,
        "duplicate_uniq_id_count": len(dup_uniq_ids),
        "distinct_pid": pid_count,
        "duplicate_pid_count": len(dup_pids),
        "distinct_product_names": product_name_count,
        "repeated_product_name_count": total_records - product_name_count,
    }


def load_processed_data(filepath: str = "data/processed/flipkart_cleaned.csv") -> pd.DataFrame:
    """Loads the cleaned processed dataset.
    
    Args:
        filepath: Relative or absolute path to cleaned CSV.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Processed dataset not found at: {filepath}")
    return pd.read_csv(path, encoding="utf-8")
