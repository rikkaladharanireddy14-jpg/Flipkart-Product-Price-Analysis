"""Exploratory Data Analysis (EDA) Script
Generates high-resolution statistical visualizations and computes comprehensive
analytical metrics on the processed Flipkart dataset.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "figure.autolayout": True,
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 1.0,
    "grid.color": "#ebebeb",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

OUTPUT_DIR = Path("reports/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("data/processed/flipkart_cleaned.csv")


def plot_01_price_distributions():
    """1. Overall Product Price Distribution (Raw & Log-scaled)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1A. Raw Retail Price (capped at 99th percentile for visual clarity)
    p99_retail = float(df["retail_price"].quantile(0.99))
    retail_subset = df[df["retail_price"] <= p99_retail]["retail_price"].to_numpy()
    sns.histplot(retail_subset, bins=40, kde=True, color="#1f77b4", ax=axes[0, 0])
    axes[0, 0].set_title(f"A. Retail Price (MRP) Distribution (<= 99th Pct: INR {p99_retail:,.0f})", fontsize=12, fontweight="bold")
    axes[0, 0].set_xlabel("Retail Price (INR)")
    axes[0, 0].set_ylabel("Product Count")
    axes[0, 0].axvline(df["retail_price"].median(), color="red", linestyle="--", label=f"Median: INR {df['retail_price'].median():,.0f}")
    axes[0, 0].legend()
    
    # 1B. Raw Discounted Price (capped at 99th percentile)
    p99_disc = float(df["discounted_price"].quantile(0.99))
    disc_subset = df[df["discounted_price"] <= p99_disc]["discounted_price"].to_numpy()
    sns.histplot(disc_subset, bins=40, kde=True, color="#2ca02c", ax=axes[0, 1])
    axes[0, 1].set_title(f"B. Discounted Selling Price Distribution (<= 99th Pct: INR {p99_disc:,.0f})", fontsize=12, fontweight="bold")
    axes[0, 1].set_xlabel("Discounted Price (INR)")
    axes[0, 1].set_ylabel("Product Count")
    axes[0, 1].axvline(df["discounted_price"].median(), color="red", linestyle="--", label=f"Median: INR {df['discounted_price'].median():,.0f}")
    axes[0, 1].legend()
    
    # 1C. Log-Transformed Retail Price
    sns.histplot(df["log_retail_price"].to_numpy(), bins=35, kde=True, color="#1f77b4", ax=axes[1, 0])
    axes[1, 0].set_title("C. Log-Transformed Retail Price [log(1 + MRP)]", fontsize=12, fontweight="bold")
    axes[1, 0].set_xlabel("Log1p(Retail Price)")
    axes[1, 0].set_ylabel("Product Count")
    axes[1, 0].axvline(df["log_retail_price"].mean(), color="black", linestyle=":", label=f"Mean: {df['log_retail_price'].mean():.2f}")
    axes[1, 0].legend()
    
    # 1D. Log-Transformed Discounted Price
    sns.histplot(df["log_discounted_price"].to_numpy(), bins=35, kde=True, color="#2ca02c", ax=axes[1, 1])
    axes[1, 1].set_title("D. Log-Transformed Selling Price [log(1 + Selling Price)]", fontsize=12, fontweight="bold")
    axes[1, 1].set_xlabel("Log1p(Discounted Price)")
    axes[1, 1].set_ylabel("Product Count")
    axes[1, 1].axvline(df["log_discounted_price"].mean(), color="black", linestyle=":", label=f"Mean: {df['log_discounted_price'].mean():.2f}")
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_price_distribution.png", dpi=300)
    plt.close()
    print("  [Saved] 01_price_distribution.png")


def plot_02_retail_vs_discounted():
    """2. Retail Price vs Discounted Price Scatter with Parity Reference"""
    plt.figure(figsize=(10, 8))
    
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)
    
    sns.scatterplot(
        data=sample_df,
        x="retail_price",
        y="discounted_price",
        hue="discount_tier",
        palette="viridis",
        alpha=0.6,
        s=30,
        edgecolor=None
    )
    
    max_val = float(min(sample_df["retail_price"].quantile(0.995), sample_df["discounted_price"].quantile(0.995)))
    plt.plot([0, max_val], [0, max_val], color="crimson", linestyle="--", linewidth=2, label="Parity Line (0% Discount, MRP = Selling)")
    
    plt.xlim(0, max_val)
    plt.ylim(0, max_val)
    plt.title("Retail Price vs Discounted Price (Sample n=5,000)", fontsize=13, fontweight="bold")
    plt.xlabel("Retail Price / MRP (INR)", fontsize=11)
    plt.ylabel("Discounted Selling Price (INR)", fontsize=11)
    plt.legend(title="Discount Tier", bbox_to_anchor=(1.05, 1), loc="upper left")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_retail_vs_discounted_price.png", dpi=300)
    plt.close()
    print("  [Saved] 02_retail_vs_discounted_price.png")


def plot_03_discount_analysis():
    """3. Discount Percentage Distribution and Tier Breakdown"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 3A. Continuous Discount Percentage Distribution
    sns.histplot(df["discount_percentage"].to_numpy(), bins=40, kde=True, color="#ff7f0e", ax=axes[0])
    axes[0].set_title("A. Discount Percentage Distribution", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Discount (%)")
    axes[0].set_ylabel("Product Count")
    axes[0].axvline(df["discount_percentage"].median(), color="blue", linestyle="--", label=f"Median: {df['discount_percentage'].median():.1f}%")
    axes[0].axvline(df["discount_percentage"].mean(), color="red", linestyle=":", label=f"Mean: {df['discount_percentage'].mean():.1f}%")
    axes[0].legend()
    
    # 3B. Discount Tier Proportions
    tier_order = [
        "No Discount (0%)",
        "Low Discount (1-25%)",
        "Moderate Discount (26-50%)",
        "High Discount (51-75%)",
        "Clearance (>75%)"
    ]
    tier_counts = [int((df["discount_tier"] == t).sum()) for t in tier_order]
    tier_pcts = [(cnt / len(df)) * 100 for cnt in tier_counts]
    
    colors = ["#2b5c8f", "#4192c7", "#fdbb84", "#e34a33", "#b30000"]
    bars = axes[1].bar(tier_order, tier_counts, color=colors, edgecolor="black", linewidth=0.8)
    axes[1].set_title("B. Products by Discount Tier", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Product Count")
    axes[1].set_xticks(range(len(tier_order)))
    axes[1].set_xticklabels(tier_order, rotation=25, ha="right")
    
    for bar, pct in zip(bars, tier_pcts):
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 100, f"{pct:.1f}%\n({int(yval):,})", ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_discount_percentage_distribution.png", dpi=300)
    plt.close()
    print("  [Saved] 03_discount_percentage_distribution.png")


def plot_04_category_pricing():
    """4. Category-Wise Pricing and Discount Depth"""
    top_cats = df["primary_category"].value_counts().head(10).index.tolist()
    cat_df = df[df["primary_category"].isin(top_cats)].copy()
    
    agg = cat_df.groupby("primary_category").agg(
        median_selling_price=("discounted_price", "median"),
        median_discount_pct=("discount_percentage", "median"),
        product_count=("uniq_id", "count")
    ).loc[top_cats].reset_index()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # 4A. Median Selling Price by Category
    sns.barplot(data=agg, y="primary_category", x="median_selling_price", palette="Blues_r", ax=axes[0])
    axes[0].set_title("A. Median Selling Price Across Top 10 Categories", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Median Selling Price (INR)")
    axes[0].set_ylabel("Primary Category")
    for i, row in agg.iterrows():
        axes[0].text(row["median_selling_price"] + 20, i, f"INR {row['median_selling_price']:,.0f}", va="center", fontsize=9, fontweight="bold")
        
    # 4B. Median Discount Percentage by Category
    sns.barplot(data=agg, y="primary_category", x="median_discount_pct", palette="Oranges_r", ax=axes[1])
    axes[1].set_title("B. Median Discount (%) Across Top 10 Categories", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Median Discount Percentage (%)")
    axes[1].set_ylabel("")
    axes[1].set_yticklabels([])
    for i, row in agg.iterrows():
        axes[1].text(row["median_discount_pct"] + 0.8, i, f"{row['median_discount_pct']:.1f}%", va="center", fontsize=9, fontweight="bold")
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_category_pricing_analysis.png", dpi=300)
    plt.close()
    print("  [Saved] 04_category_pricing_analysis.png")


def plot_05_brand_analysis():
    """5. Brand Pricing Power & Volume Analysis"""
    brand_counts = df[df["brand"] != "Unbranded / Generic"]["brand"].value_counts()
    top_brands = brand_counts.head(12).index.tolist()
    
    b_df = df[df["brand"].isin(top_brands)].copy()
    b_agg = b_df.groupby("brand").agg(
        median_selling=("discounted_price", "median"),
        median_discount=("discount_percentage", "median"),
        count=("uniq_id", "count")
    ).loc[top_brands].reset_index()
    
    plt.figure(figsize=(12, 6))
    scatter = plt.scatter(
        b_agg["median_discount"],
        b_agg["median_selling"],
        s=b_agg["count"] * 2.5,
        c=b_agg["median_discount"],
        cmap="coolwarm",
        alpha=0.8,
        edgecolors="black",
        linewidth=1.2
    )
    
    for _, row in b_agg.iterrows():
        plt.annotate(
            f"{row['brand']}\n(n={int(row['count'])})",
            (row["median_discount"], row["median_selling"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=8,
            fontweight="bold"
        )
        
    plt.colorbar(scatter, label="Median Discount (%)")
    plt.title("Brand Pricing Power: Median Selling Price vs Discount % (Top 12 Brands)", fontsize=13, fontweight="bold")
    plt.xlabel("Median Discount (%)", fontsize=11)
    plt.ylabel("Median Selling Price (INR)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_brand_pricing_power.png", dpi=300)
    plt.close()
    print("  [Saved] 05_brand_pricing_power.png")


def plot_06_rating_analysis():
    """6. Product Rating Distribution & Price Correlation"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    rated_df = df[df["is_rated"] == 1].copy()
    
    # 6A. Rating Score Distribution
    sns.histplot(rated_df["rating_score"].to_numpy(), bins=15, kde=True, color="#9467bd", ax=axes[0])
    axes[0].set_title(f"A. Customer Rating Distribution (n = {len(rated_df):,} Rated Products)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Star Rating (1.0 to 5.0)")
    axes[0].set_ylabel("Product Count")
    axes[0].axvline(rated_df["rating_score"].median(), color="red", linestyle="--", label=f"Median: {rated_df['rating_score'].median():.1f}")
    axes[0].axvline(rated_df["rating_score"].mean(), color="blue", linestyle=":", label=f"Mean: {rated_df['rating_score'].mean():.2f}")
    axes[0].legend()
    
    # 6B. Discount % by Rating Integer Buckets
    rated_df["rating_band"] = rated_df["rating_score"].apply(lambda r: f"{int(np.floor(r))}* to {int(np.floor(r))+1}*" if r < 5.0 else "5.0*")
    band_order = ["1* to 2*", "2* to 3*", "3* to 4*", "4* to 5*", "5.0*"]
    
    sns.boxplot(data=rated_df, x="rating_band", y="discount_percentage", order=band_order, palette="Purples", ax=axes[1])
    axes[1].set_title("B. Discount Percentage Across Rating Bands", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Rating Band")
    axes[1].set_ylabel("Discount Percentage (%)")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_rating_distribution_and_price.png", dpi=300)
    plt.close()
    print("  [Saved] 06_rating_distribution_and_price.png")


def plot_07_correlation_matrix():
    """7. Correlation Matrix of Numerical Attributes"""
    plt.figure(figsize=(10, 8))
    
    corr_cols = [
        "retail_price",
        "discounted_price",
        "discount_amount",
        "discount_percentage",
        "log_retail_price",
        "log_discounted_price",
        "product_name_word_count",
        "description_word_count",
        "is_FK_Advantage_product",
        "is_rated"
    ]
    
    corr = df[corr_cols].corr()
    
    labels = [
        "Retail Price (MRP)",
        "Discounted Price",
        "Discount (INR)",
        "Discount (%)",
        "Log(MRP)",
        "Log(Selling)",
        "Name Words",
        "Desc Words",
        "FK Advantage",
        "Is Rated (0/1)"
    ]
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        xticklabels=labels,
        yticklabels=labels,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation Heatmap of Numerical Features", fontsize=13, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "07_correlation_matrix.png", dpi=300)
    plt.close()
    print("  [Saved] 07_correlation_matrix.png")


if __name__ == "__main__":
    print("Generating EDA Visualizations...")
    plot_01_price_distributions()
    plot_02_retail_vs_discounted()
    plot_03_discount_analysis()
    plot_04_category_pricing()
    plot_05_brand_analysis()
    plot_06_rating_analysis()
    plot_07_correlation_matrix()
    print("All 7 EDA figures successfully generated in reports/figures/")
