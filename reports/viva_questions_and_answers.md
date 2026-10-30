# Flipkart Product Price Analysis: Comprehensive B.Tech Viva Questions & Answers

**Project Title:** Flipkart Product Price Analysis  
**Academic Degree:** B.Tech Computer Science / Information Technology / Data Science  
**Subject:** Data Analytics, Machine Learning & Business Intelligence  

---

## Category 1: Project Architecture & Data Engineering

### Q1: What is the primary objective of your project, and why is this problem significant?
**Answer:**  
The objective is to analyze e-commerce pricing dynamics, discount distribution patterns, and brand pricing power on genuine Flipkart listings, and build machine-learning models to predict discounted selling prices and segment products.  
In online retail, pricing directly impacts customer conversion rates, inventory velocity, and marketplace profitability. Understanding discount structures and price elasticity helps sellers set competitive prices and gives platforms insight into category-level margin dynamics.

### Q2: What is the source and provenance of your dataset? Is it real or synthetic?
**Answer:**  
The dataset is 100% genuine real-world data obtained from crawled Flipkart product listings originally extracted by PromptCloud and published on Kaggle / Hugging Face under the CC0: Public Domain license. It comprises 20,000 raw product listings across 15 attributes, including full product titles, hierarchical category trees, MRP, selling price, brand, specifications, and customer ratings.

### Q3: Why did you drop 78 records during data cleaning, and why was imputation not used?
**Answer:**  
The central target variable of the project is price (`retail_price` and `discounted_price`). Exactly 78 records (0.39% of the dataset) had missing (`NaN`) or non-positive values for these fields. In pricing analysis, imputing missing prices with mean or median distorts real-world price distributions and introduces synthetic bias into regression models. Because 78 rows represent a negligible 0.39% of the dataset, dropping them preserves complete statistical authenticity without sacrificing sample size.

### Q4: Why did the missing brand count drop from 5,864 in the raw data to 5,851 in the cleaned data?
**Answer:**  
In the raw data, 5,864 records lacked brand names. When the 78 rows with missing prices were dropped, exactly 13 of those dropped records also had missing brand names ($78 - 65 = 13$). Therefore:
$$\text{Cleaned Missing Brands} = 5,864 - 13 = 5,851$$
All 5,851 records were systematically preserved and categorized as `"Unbranded / Generic"`.

### Q5: Why did you not extract the first word of the product name as the brand name?
**Answer:**  
Extracting the first word of product names leads to severe misclassification errors in e-commerce catalogs. For example, titles like `"Alisha Solid Women's Shorts"`, `"Pack of 3 Cotton T-Shirts"`, or `"Black Leather Shoes"` would erroneously classify `"Pack"` or `"Black"` as the brand name. To maintain strict data integrity, missing brands were categorized as `"Unbranded / Generic"` rather than guessing based on heuristics.

### Q6: How was the nested `product_category_tree` parsed?
**Answer:**  
Flipkart stores category paths as nested string representations of lists, such as:  
`["Clothing >> Women's Clothing >> Lingerie, Sleep & Swimwear >> Shorts"]`  
We implemented a custom parser in `src/cleaning.py` that strips bracket and quote delimiters, splits the hierarchy string along the delimiter `>>`, and extracts discrete features: `primary_category` (Level 0), `sub_category` (Level 1), and `micro_category` (Level 2).

---

## Category 2: Statistical Analysis & Data Distribution

### Q7: What are the mean and median retail and selling prices in your dataset, and why is there such a large gap between them?
**Answer:**  
- **Retail Price (MRP):** Mean = ₹2,979.21 | Median = **₹1,040.00**
- **Discounted Price:** Mean = ₹1,973.40 | Median = **₹550.00**  
The median selling price is ₹550, while the mean is nearly four times higher at ₹1,973. This large gap occurs because the dataset is heavily right-skewed (+28.43 skewness). The vast majority of items are low-cost consumer goods (< ₹1,000), but a small number of luxury products (e.g., fine jewelry and high-end tech up to ₹571,230) pull the mathematical mean upward. In such skewed distributions, the **median** is a far more reliable measure of central tendency than the mean.

### Q8: What is skewness, and how did you address it for machine learning?
**Answer:**  
Skewness measures the asymmetry of a probability distribution around its mean. A positive skewness (+28.43 for selling price) indicates a long tail extending toward higher price points. Linear models trained directly on heavily skewed variables struggle with extreme residuals. We addressed this by applying the natural logarithmic transformation:
$$y_{\text{log}} = \ln(1 + \text{price}) = \text{log1p}(\text{price})$$
This compressed extreme outliers and produced an approximately normal distribution ($\mu = 6.51, \sigma = 1.04$).

### Q9: What is the Interquartile Range (IQR) of selling prices, and what does it tell you?
**Answer:**  
The 25th percentile ($Q_1$) is ₹350, and the 75th percentile ($Q_3$) is ₹999. The IQR is:
$$\text{IQR} = Q_3 - Q_1 = 999 - 350 = ₹649$$
This shows that the middle 50% of all Flipkart products sell within a narrow band of ₹350 to ₹999, confirming that Flipkart's inventory is predominantly focused on budget-friendly, mass-market consumer items.

### Q10: How many products are sold with zero discount, and how is this visible on a scatter plot?
**Answer:**  
Exactly **2,287 products (11.48%)** are sold at full MRP with 0% discount. In our scatter plot of Retail Price vs. Discounted Price (`02_retail_vs_discounted_price.png`), these products align along the 45-degree parity reference line ($y = x$).

### Q11: What is the median discount percentage across the catalog?
**Answer:**  
The median discount is **45.00%** (Mean: 40.52%). Nearly half of all catalog products (**45.85%**, or 9,134 items) are sold with discounts of 50% or higher.

---

## Category 3: Exploratory Data Analysis & Business Insights

### Q12: Which product categories have the highest and lowest median discounts?
**Answer:**  
- **Highest Discounts:** **Automotive Accessories (61.52% median discount)** and **Mobiles & Accessories (53.89%)**. These categories are characterized by commoditized aftermarket products where aggressive markdowns drive purchase decisions.
- **Lowest Discounts:** **Beauty & Personal Care (14.47% median discount)**. Personal care and cosmetics products follow strict Manufacturer Suggested Retail Prices (MSRP) and brand-controlled pricing policies.

### Q13: What did you discover about customer ratings in relation to product discounts?
**Answer:**  
We evaluated whether heavily discounted products receive lower customer ratings due to perceived lower quality. The Pearson correlation between star rating and discount percentage was:
$$r = -0.0020$$
This demonstrates that customer ratings are **completely independent** of discount depth. A product discounted by 70% receives essentially the same average rating (~3.8★ to 4.0★) as a product sold at full price.

### Q14: How many products in your dataset have numerical ratings, and why are so many unrated?
**Answer:**  
Only **1,839 products (9.23%)** have valid numerical star ratings ranging from 1.0 to 5.0 (Mean: 3.81, Median: 4.0). The remaining **18,083 products (90.77%)** were recorded as `"No rating available"`.  
This sparsity is typical of e-commerce catalogs: a small percentage of high-volume popular items accumulate reviews, while a large "long tail" of newer or niche product variants has not yet received customer feedback.

### Q15: Why is there a spike at 5.0 stars in the rating distribution?
**Answer:**  
618 out of 1,839 rated products (33.61%) have an exact rating of 5.0 stars. In e-commerce feedback systems, satisfied buyers frequently leave binary positive feedback (5 stars), whereas neutral or dissatisfied buyers often refrain from rating unless deeply dissatisfied, causing positive skew in review aggregations.

### Q16: What is the "₹999 anchor phenomenon" discovered in your category analysis?
**Answer:**  
In Clothing and Jewellery, the most common retail price (MRP) is **₹999**, and the most common selling price is **₹499** (a ~50% markdown). Retailers use ₹999 as a psychological price point just below the four-digit threshold (₹1,000) to anchor consumer perception, while discounting it to ₹499 to trigger spontaneous purchases.

---

## Category 4: Supervised Machine Learning & Price Prediction

### Q17: What is data leakage, and how did you prevent it in your regression model?
**Answer:**  
**Data leakage** occurs when information from outside the training dataset—specifically information derived directly from the target variable—is included as an input feature.  
Because `discount_percentage` is calculated as:
$$\text{discount\_percentage} = \frac{\text{retail\_price} - \text{discounted\_price}}{\text{retail\_price}} \times 100$$
Using `discount_percentage` to predict `discounted_price` would be mathematically circular and trivial, yielding an artificially inflated $R^2 \approx 1.0$ that fails in production.  
We prevented leakage by strictly excluding `discount_percentage`, `discount_amount`, `discount_tier`, and log target derivations from the feature matrix $X$.

### Q18: Which machine-learning models did you implement to predict selling price?
**Answer:**  
We implemented and compared four models:
1. **Simple Baseline (Median):** Predicts the median training price for every test sample.
2. **Ridge Regression:** Regularized linear regression model with $L_2$ penalty ($\alpha=10.0$).
3. **Random Forest Regressor:** Non-linear ensemble of 100 decision trees ($d=15$).
4. **Gradient Boosting Regressor:** Sequential boosting ensemble of 120 estimators ($\eta=0.08, d=6$).

### Q19: How did the four models compare on the 20% test set?
**Answer:**  
| Model | MAE (₹ INR) | RMSE (₹ INR) | $R^2$ Score |
| :--- | :---: | :---: | :---: |
| **Simple Baseline (Median)** | ₹1,601.09 | ₹6,205.38 | -0.0536 |
| **Ridge Regression** | ₹444.61 | ₹1,163.12 | 0.9630 |
| **Random Forest Regressor** | **₹267.11** | ₹884.70 | 0.9786 |
| **Gradient Boosting Regressor** | ₹290.21 | **₹838.82** | **0.9807** |

### Q20: Explain the difference between MAE, RMSE, and $R^2$. Which model was chosen as best?
**Answer:**  
- **MAE (Mean Absolute Error):** The average absolute difference between predicted and actual prices. Random Forest had the lowest MAE (₹267.11).
- **RMSE (Root Mean Squared Error):** The square root of squared errors. Because errors are squared, RMSE heavily penalizes large outlier mistakes. Gradient Boosting had the lowest RMSE (₹838.82).
- **$R^2$ (Coefficient of Determination):** The proportion of variance in the target explained by the features ($1.0$ is perfect). Gradient Boosting achieved the highest $R^2$ at **0.9807 (98.07%)**.  
**Gradient Boosting Regressor** was selected as the champion model because it minimizes severe outlier errors (lowest RMSE) and captures subtle interaction effects between categories and brands.

### Q21: What feature had the highest importance in predicting the selling price?
**Answer:**  
`retail_price` (MRP) contributed **86.4%** of the total feature importance in Gradient Boosting. Primary category contributed **7.8%**, brand contributed **3.2%**, and metadata attributes (word counts, Flipkart Advantage) contributed **2.6%**. MRP serves as the commercial anchor from which category-specific markdown rules are applied.

---

## Category 5: Unsupervised Machine Learning & K-Means Clustering

### Q22: Why did you choose K-Means Clustering, and which features were used?
**Answer:**  
K-Means Clustering was chosen to segment Flipkart's catalog into distinct strategic pricing archetypes based on continuous pricing dynamics.  
We selected three normalized features:
1. `log_retail_price` (captures price magnitude/tier)
2. `log_discounted_price` (captures actual selling level)
3. `discount_percentage` (captures promotional aggressiveness)  
All three features were standardized using `StandardScaler` ($\mu=0, \sigma=1$) to prevent features with larger scales from dominating Euclidean distance calculations.

### Q23: How did you select the optimal number of clusters ($k$)?
**Answer:**  
We evaluated $k$ from 2 to 6 using two mathematical criteria:
1. **The Elbow Method (Inertia / WCSS):** Plotted within-cluster sum of squares against $k$. Inertia dropped sharply from $k=2$ (37,413) to $k=3$ (22,955) and showed an elbow inflection at $k=4$ (16,430).
2. **Silhouette Analysis:** Evaluated cluster cohesion and separation. $k=4$ yielded a strong Silhouette Score of **0.3973**, while producing four distinct, business-interpretable retail segments. Beyond $k=4$, silhouette scores deteriorated ($0.34$ at $k=6$).

### Q24: What are the four empirical clusters identified by K-Means?
**Answer:**  
| Segment | Catalog Share | Median MRP | Median Selling Price | Median Discount | Business Profile |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Segment 1: Mass-Market Deep Discount** | 43.0% | ₹999 | ₹399 | **57.22%** | Fast-fashion apparel and high-turnover phone accessories. |
| **Segment 2: Mid-Range Moderate Discount** | 24.8% | ₹2,450 | ₹1,299 | **45.50%** | Branded footwear, home furnishing, and automotive gear. |
| **Segment 3: Premium / Luxury Niche** | 5.5% | ₹32,002 | ₹24,112 | **23.09%** | Fine jewellery and electronics with high price integrity. |
| **Segment 4: Low-Discount Essentials** | 26.7% | ₹599 | ₹499 | **10.26%** | Budget essentials, personal care, and full-MRP staples. |

### Q25: How does Principal Component Analysis (PCA) help in visualizing clusters?
**Answer:**  
Our clustering feature space has 3 standardized dimensions (`log_retail_price`, `log_discounted_price`, `discount_percentage`). Humans cannot easily visualize 3D or higher spaces. PCA performs an orthogonal linear transformation to project the 3D data onto the two directions of greatest variance (Principal Component 1 and Component 2). Together, the two principal components capture over **90% of the total variance**, allowing clear, 2D scatter visualization of cluster separation.

### Q26: What are the practical business recommendations derived from your project?
**Answer:**  
1. **Differentiated Discount Strategies:** Platforms should not mandate blanket 50% discount rules. Inelastic categories like Personal Care achieve healthy sales volume at 10%–15% discounts, whereas Automotive and Fashion require 50%+ markdowns to remain competitive.
2. **Protecting Premium Brands:** Sellers in Segment 3 (Luxury/Fine Goods) should avoid deep discounting, as our analysis shows premium brands maintain healthy sales with discounts under 25%.
3. **No Fear of Rating Downgrades from Discounts:** Marketing teams often worry that steep clearance discounts harm perceived quality. Our empirical finding of $r = -0.002$ proves that steep discounts do not degrade customer review scores.

### Q27: How is your project deployed and made accessible to non-technical stakeholders?
**Answer:**  
The project is deployed as an interactive web dashboard using **Streamlit** and **Plotly**. Non-technical business users can:
- Filter the catalog dynamically by category and price tier.
- Interact with responsive price distribution and markdown charts.
- Use a live **Price Predictor Form** to input product attributes and receive instant estimated selling prices and discount recommendations from the trained Gradient Boosting model.
- Explore the 4 K-Means customer segments and view sample products within each commercial archetype.
