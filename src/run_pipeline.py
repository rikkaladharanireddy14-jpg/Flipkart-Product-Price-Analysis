"""Pipeline Execution Script
Executes the end-to-end data cleaning and feature engineering workflow,
saves data/processed/flipkart_cleaned.csv, and produces an audit report.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_loader import load_raw_data, audit_identifiers
from src.cleaning import clean_flipkart_data
from src.feature_engineering import add_pricing_features


def run_pipeline() -> None:
    print("=" * 70)
    print("  FLIPKART PRODUCT PRICE ANALYSIS: DATA CLEANING & FEATURE PIPELINE")
    print("=" * 70)
    
    # 1. Load raw data
    print("\n[Step 1/5] Loading original raw dataset...")
    df_raw = load_raw_data("data/raw/flipkart_com-ecommerce_sample.csv")
    print(f"  Loaded {len(df_raw):,} records with {df_raw.shape[1]} columns.")
    
    # 2. Audit identifiers
    print("\n[Step 2/5] Auditing raw identifiers...")
    audit = audit_identifiers(df_raw)
    print(f"  Total records: {audit['total_records']:,}")
    print(f"  Distinct uniq_ids: {audit['distinct_uniq_id']:,} (Duplicates: {audit['duplicate_uniq_id_count']})")
    print(f"  Distinct pids: {audit['distinct_pid']:,} (Duplicates: {audit['duplicate_pid_count']})")
    print(f"  Distinct product names: {audit['distinct_product_names']:,} (Repeated titles: {audit['repeated_product_name_count']:,})")
    print("  * Note: Products sharing names are preserved as legitimate seller/variant listings.")
    
    # 3. Clean dataset
    print("\n[Step 3/5] Cleaning dataset and applying domain validation...")
    df_clean, clean_stats = clean_flipkart_data(df_raw)
    print(f"  Dropped records with invalid/missing price: {clean_stats['dropped_invalid_price_rows']}")
    print(f"  Clean records: {clean_stats['final_clean_rows']:,}")
    print(f"  Rated products: {clean_stats['rated_products_count']:,} ({clean_stats['rated_percentage']}%)")
    print(f"  Unrated products: {clean_stats['unrated_products_count']:,} ({100 - clean_stats['rated_percentage']:.2f}%)")
    print(f"  Unbranded / Generic products: {clean_stats['unbranded_products_count']:,}")
    print(f"  Distinct primary categories: {clean_stats['distinct_primary_categories']}")
    print(f"  Distinct brands: {clean_stats['distinct_brands']}")
    
    # 4. Feature engineering
    print("\n[Step 4/5] Engineering analytical features & price tiers...")
    df_featured = add_pricing_features(df_clean)
    print(f"  Features successfully created. Final column count: {df_featured.shape[1]}")
    
    # 5. Export processed dataset
    output_path = Path("data/processed/flipkart_cleaned.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_featured.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n[Step 5/5] Exported cleaned dataset to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")
    print("=" * 70)
    print("  PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
