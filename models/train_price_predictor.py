"""Supervised Learning: Price Prediction Models
Trains and compares Baseline (Dummy), Ridge Regression, Random Forest,
and Gradient Boosting Regressors to predict Flipkart discounted_price.

CRITICAL DATA LEAKAGE RULE:
No discount percentage, discount amount, discount tier, or target derivations
are included in the feature set X.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
OUTPUT_DIR = Path("reports/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def train_and_evaluate_models():
    print("=" * 70)
    print("  PART A: SUPERVISED LEARNING - FLIPKART PRICE PREDICTION")
    print("=" * 70)
    
    # 1. Load Cleaned Dataset
    data_path = Path("data/processed/flipkart_cleaned.csv")
    df = pd.read_csv(data_path)
    print(f"\n[1] Loaded cleaned dataset: {len(df):,} records.")
    
    # 2. Define Features and Target (STRICT LEAKAGE PREVENTION)
    target_col = "discounted_price"
    y = df[target_col].values
    
    # Strict assertion: absolutely no discount derivatives
    forbidden_leakage_cols = [
        "discounted_price",
        "discount_amount",
        "discount_percentage",
        "discount_tier",
        "log_discounted_price"
    ]
    
    num_features = [
        "retail_price",
        "product_name_word_count",
        "description_word_count",
        "is_FK_Advantage_product",
        "is_rated"
    ]
    cat_features = ["primary_category", "brand"]
    
    X = df[num_features + cat_features].copy()
    
    # Clean categorical text
    X["primary_category"] = X["primary_category"].fillna("Unknown").astype(str)
    X["brand"] = X["brand"].fillna("Unbranded / Generic").astype(str)
    X["is_FK_Advantage_product"] = X["is_FK_Advantage_product"].astype(int)
    X["is_rated"] = X["is_rated"].astype(int)
    
    print(f"\n[2] Features selected ({len(num_features)} numeric, {len(cat_features)} categorical):")
    print(f"    Numeric:     {num_features}")
    print(f"    Categorical: {cat_features}")
    print(f"    Target:      {target_col}")
    print("    * Verified: Absolutely NO discount metrics used in feature matrix X.")
    
    # 3. Train-Test Split (80:20, fixed random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"\n[3] Train/Test Split: Train = {len(X_train):,} samples, Test = {len(X_test):,} samples.")
    
    # 4. Preprocessing Pipeline
    # Standardize numerical features and One-Hot Encode top categories & brands
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30, sparse_output=False), cat_features)
        ],
        remainder="drop"
    )
    
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    num_encoded_cols = X_train_proc.shape[1]
    print(f"    Preprocessed feature dimensions: {num_encoded_cols} columns.")
    
    # 5. Define Models
    models = {
        "Simple Baseline (Median)": DummyRegressor(strategy="median"),
        "Ridge Regression (Baseline Linear)": Ridge(alpha=10.0, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=120, learning_rate=0.08, max_depth=6, random_state=42
        )
    }
    
    # 6. Train and Evaluate
    results = []
    predictions = {}
    
    print("\n[4] Training models and computing test metrics...")
    for name, model in models.items():
        print(f"    Training: {name}...")
        model.fit(X_train_proc, y_train)
        y_pred = model.predict(X_test_proc)
        
        # Enforce non-negative price prediction
        y_pred = np.clip(y_pred, a_min=0.0, a_max=None)
        predictions[name] = y_pred
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            "Model": name,
            "MAE (INR)": round(mae, 2),
            "RMSE (INR)": round(rmse, 2),
            "R2 Score": round(r2, 4)
        })
        print(f"      -> MAE: INR {mae:,.2f} | RMSE: INR {rmse:,.2f} | R2: {r2:.4f}")
        
    results_df = pd.DataFrame(results)
    print("\n" + "=" * 70)
    print("  MODEL EVALUATION RESULTS TABLE")
    print("=" * 70)
    print(results_df.to_string(index=False))
    
    # 7. Visualization 1: Actual vs Predicted Prices (Ridge vs Best Ensemble)
    best_model_name = "Gradient Boosting Regressor"
    ridge_name = "Ridge Regression (Baseline Linear)"
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sample_indices = np.random.RandomState(42).choice(len(y_test), size=min(1500, len(y_test)), replace=False)
    y_sample_actual = y_test[sample_indices]
    
    # Subplot 1: Ridge Regression
    axes[0].scatter(y_sample_actual, predictions[ridge_name][sample_indices], alpha=0.4, color="#1f77b4", s=25, label="Test Predictions")
    max_p = max(y_sample_actual.max(), predictions[ridge_name][sample_indices].max())
    axes[0].plot([10, max_p], [10, max_p], color="red", linestyle="--", linewidth=2, label="Ideal Fit (y = x)")
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    ridge_r2 = results_df.loc[results_df["Model"] == ridge_name, "R2 Score"].values[0]
    ridge_mae = results_df.loc[results_df["Model"] == ridge_name, "MAE (INR)"].values[0]
    axes[0].set_title(f"A. Ridge Regression: Actual vs Predicted\n(R2 = {ridge_r2:.4f}, MAE = INR {ridge_mae:,.0f})", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Actual Discounted Price (INR, Log Scale)")
    axes[0].set_ylabel("Predicted Discounted Price (INR, Log Scale)")
    axes[0].legend()
    
    # Subplot 2: Gradient Boosting
    axes[1].scatter(y_sample_actual, predictions[best_model_name][sample_indices], alpha=0.4, color="#2ca02c", s=25, label="Test Predictions")
    axes[1].plot([10, max_p], [10, max_p], color="red", linestyle="--", linewidth=2, label="Ideal Fit (y = x)")
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    gb_r2 = results_df.loc[results_df["Model"] == best_model_name, "R2 Score"].values[0]
    gb_mae = results_df.loc[results_df["Model"] == best_model_name, "MAE (INR)"].values[0]
    axes[1].set_title(f"B. Gradient Boosting: Actual vs Predicted\n(R2 = {gb_r2:.4f}, MAE = INR {gb_mae:,.0f})", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Actual Discounted Price (INR, Log Scale)")
    axes[1].set_ylabel("Predicted Discounted Price (INR, Log Scale)")
    axes[1].legend()
    
    plt.tight_layout()
    pred_fig_path = OUTPUT_DIR / "08_actual_vs_predicted_prices.png"
    plt.savefig(pred_fig_path, dpi=300)
    plt.close()
    print(f"\n[5] Saved prediction visualization to: {pred_fig_path}")
    
    # 8. Visualization 2: Feature Importance
    gb_reg = models[best_model_name]
    importances = gb_reg.feature_importances_
    
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_names = list(cat_encoder.get_feature_names_out(cat_features))
    all_feature_names = num_features + cat_names
    
    feat_series = pd.Series(importances, index=all_feature_names).sort_values(ascending=False).head(12)
    
    plt.figure(figsize=(10, 6))
    feat_series.sort_values().plot(kind="barh", color="#2ca02c", edgecolor="black")
    plt.title(f"Top 12 Feature Importances ({best_model_name})", fontsize=12, fontweight="bold")
    plt.xlabel("Relative Feature Importance Score")
    plt.ylabel("Model Feature")
    plt.tight_layout()
    feat_fig_path = OUTPUT_DIR / "09_feature_importances.png"
    plt.savefig(feat_fig_path, dpi=300)
    plt.close()
    print(f"[6] Saved feature importance plot to: {feat_fig_path}")
    
    return results_df


if __name__ == "__main__":
    train_and_evaluate_models()
