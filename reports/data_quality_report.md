# Flipkart Product Price Analysis: Data Quality & Validation Report

**Project:** B.Tech Data Analytics Project - Flipkart Product Price Analysis  
**Date:** October 30, 2026  
**Target Environment:** Python 3.10.1 (64-bit)  
**Processed File:** `data/processed/flipkart_cleaned.csv`  
**Raw Source File:** `data/raw/flipkart_com-ecommerce_sample.csv`  

---

## 1. Executive Summary & Raw Dataset Integrity

The original raw dataset was obtained from genuine crawled Flipkart listings published by PromptCloud on Kaggle / Hugging Face under the CC0: Public Domain license. It represents an immutable benchmark dataset containing 20,000 product rows across 15 attributes.

### Raw Dataset Verification
- **File Path:** `data/raw/flipkart_com-ecommerce_sample.csv`
- **File Size:** 38,114,963 bytes (~36.35 MB)
- **SHA256 Checksum:** `56F8F699C9E847356666C2EAB3C3AB1244340F6A98AD08E39EA2199EBE993AD1`
- **Integrity Status:** Strictly unchanged and preserved in read-only mode.

---

## 2. Before-and-After Cleaning Statistics

| Metric | Raw Dataset (`data/raw/`) | Processed Dataset (`data/processed/`) | Net Change / Explanation |
| :--- | :---: | :---: | :--- |
| **Total Rows** | 20,000 | **19,922** | **-78 rows (-0.39%)**: dropped due to missing/invalid prices (`retail_price` or `discounted_price` is NaN). |
| **Total Columns** | 15 | **31** | **+16 columns**: hierarchical categories, rating metrics, discount metrics, price tiers, and log transforms. |
| **Missing `retail_price`** | 78 | **0** | Clean positive continuous numeric values. |
| **Missing `discounted_price`**| 78 | **0** | Clean positive continuous numeric values. |
| **Missing `brand`** | 5,864 | **0** | All missing brands preserved as `"Unbranded / Generic"` (see reconciliation below). |
| **Rated Products** | 1,849 (9.25%) | **1,839 (9.23%)** | Exactly 10 rated items lacked pricing and were dropped; 1,839 preserved. |
| **Unrated Products** | 18,151 (90.75%) | **18,083 (90.77%)** | Explicitly flagged with `is_rated = 0` (converted from `"No rating available"`). |

---

## 3. Brand & Rating Reconciliation

### A. Missing Brand Reconciliation
- **Raw Missing Brands:** 5,864 rows lacked brand names.
- **Dropped Records with Missing Brand:** Exactly **13** of the 78 dropped invalid-price rows lacked brand names ($78 - 65 = 13$).
- **Clean "Unbranded / Generic" Count:** $5,864 - 13 = \mathbf{5,851}$ rows.
- **Rule Enforced:** In strict accordance with data governance standards, product titles were **not** arbitrarily parsed for brands. Missing brands are transparently categorized as `"Unbranded / Generic"`.

### B. Rating Transparency
- **Raw Numerical Ratings:** 1,849 items had numeric ratings (1.0 to 5.0 stars).
- **Dropped Records with Rating:** Exactly **10** rated items had missing pricing and were dropped.
- **Clean Rated Cohort:** **1,839 items** (9.23% of the dataset) have valid numerical rating scores (Mean: 3.81, Median: 4.00).
- **Unrated Cohort:** **18,083 items** (90.77%) are flagged with `is_rated = 0`.

---

## 4. Tiers & Boundary Validation

Every valid record in `data/processed/flipkart_cleaned.csv` belongs to **exactly one** discount tier and **exactly one** price tier without gaps, overlaps, or nulls.

### Discount Tiers ($\sum = 19,922$, Nulls = 0)
- **No Discount (0%):** 2,287 products (11.48%) — sold strictly at full MRP ($d = 0$).
- **Low Discount (1% – 25%):** 3,197 products (16.05%) — ($0 < d \le 25$).
- **Moderate Discount (26% – 50%):** 5,653 products (28.38%) — ($25 < d \le 50$).
- **High Discount (51% – 75%):** 7,974 products (40.03%) — ($50 < d \le 75$).
- **Clearance (> 75%):** 811 products (4.07%) — ($75 < d \le 100$).

### Retail Price Tiers ($\sum = 19,922$, Nulls = 0)
- **Budget (< ₹500):** 3,140 products (15.76%)
- **Economy (₹500 – ₹1,500):** 9,996 products (50.18%)
- **Mid-Range (₹1,500 – ₹5,000):** 5,465 products (27.43%)
- **Premium (₹5,000 – ₹15,000):** 525 products (2.64%)
- **Luxury (> ₹15,000):** 796 products (4.00%)

---

## 5. Statistical Profile of Processed Dataset

| Column | Min | 25% (Q1) | Median (50%) | 75% (Q3) | Max | Mean | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `retail_price` (₹) | 35.00 | 666.00 | 1,040.00 | 1,999.00 | 571,230.00 | 2,979.21 | 9,004.98 |
| `discounted_price` (₹) | 35.00 | 350.00 | 550.00 | 999.00 | 571,230.00 | 1,973.40 | 7,333.68 |
| `discount_percentage` (%) | 0.00 | 21.05 | 45.00 | 59.97 | 96.53 | 40.52 | 22.75 |
| `rating_score` (Rated items) | 1.00 | 3.30 | 4.00 | 4.50 | 5.00 | 3.81 | 0.86 |
| `log_retail_price` | 3.58 | 6.50 | 6.95 | 7.60 | 13.26 | 7.15 | 1.08 |
| `log_discounted_price` | 3.58 | 5.86 | 6.31 | 6.91 | 13.26 | 6.51 | 1.04 |

---

## 6. Installed Python Environment Verification

| Library | Verified Version | Purpose |
| :--- | :---: | :--- |
| **pandas** | `2.3.3` | Tabular data wrangling, cleaning & aggregation |
| **numpy** | `1.22.4` | Vectorized numerical operations & log transformations |
| **seaborn** | `0.13.2` | Statistical visualizations & distribution plots |
| **matplotlib** | `3.5.1` | Base plotting, figure export & report styling |
| **scikit-learn** | `1.0.2` | ML modeling, feature scaling & regression (Phase 3B) |
| **streamlit** | `1.40.1` | Interactive analytics web application (Phase 4) |
