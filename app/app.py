"""Flipkart Product Price Analysis - Interactive Streamlit Dashboard
Built for B.Tech Data Analytics Project Presentation.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import joblib

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Flipkart Product Price Analysis",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Blue & White Styling (Flipkart Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a365d;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        text-align: center;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #2874f0;
    }
    .metric-label {
        font-size: 0.88rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .insight-box {
        background-color: #ebf4ff;
        border-left: 4px solid #2874f0;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
        color: #1a365d;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 4px 4px 0 0;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA & MODEL ARTIFACT CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_dataset():
    data_path = Path("data/processed/flipkart_cleaned.csv")
    if not data_path.exists():
        st.error(f"Processed dataset not found at: {data_path}")
        st.stop()
    df = pd.read_csv(data_path)
    return df


@st.cache_resource
def load_ml_artifacts():
    model_path = Path("models/saved/price_model_artifacts.joblib")
    if model_path.exists():
        return joblib.load(model_path)
    return None


df = load_dataset()
ml_artifacts = load_ml_artifacts()

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/flipkart.png", width=64)
st.sidebar.title("Flipkart Analytics")
st.sidebar.caption("B.Tech Data Analytics Project")

menu_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home / Project Overview",
        "📋 Data Overview & Dictionary",
        "💰 Price Analysis",
        "🏷️ Discount Analysis",
        "⭐ Rating Analysis",
        "🤖 Machine Learning & Prediction",
        "💡 Insights & Conclusion"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("""
**Dataset Specs:**
- **Source:** Flipkart Crawled Listings
- **Records:** 19,922 products
- **Features:** 31 attributes
- **Target:** Selling Price (INR)
""")


# -----------------------------------------------------------------------------
# PAGE 1: HOME / PROJECT OVERVIEW
# -----------------------------------------------------------------------------
if menu_choice == "🏠 Home / Project Overview":
    st.markdown('<div class="main-header">Flipkart Product Price Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">An End-to-End Data Analytics and Predictive Modeling System for E-Commerce Pricing</div>', unsafe_allow_html=True)
    
    # KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Clean Products</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{df['discounted_price'].median():,.0f}</div>
            <div class="metric-label">Median Selling Price</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df['discount_percentage'].median():.1f}%</div>
            <div class="metric-label">Median Discount</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df['primary_category'].nunique()}</div>
            <div class="metric-label">Product Categories</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Abstract & Project Objectives
    col_left, col_right = st.columns([1.2, 0.8])
    with col_left:
        st.subheader("📌 Project Abstract & Objectives")
        st.markdown("""
        In competitive retail e-commerce, **pricing dynamics** and **discount optimization** govern consumer purchasing decisions, seller inventory velocity, and marketplace profitability.
        
        This project investigates genuine Flipkart e-commerce listings across hundreds of categories to:
        1. **Profile Price Distributions:** Understand price asymmetry, skewness, and category-level markups.
        2. **Audit Discount Strategies:** Quantify markdown depths, clearance brackets, and brand pricing power.
        3. **Evaluate Reputation Elasticity:** Statistically examine whether customer star ratings influence or correlate with price markdowns.
        4. **Predict Selling Prices:** Build high-accuracy supervised regression models without feature leakage ($R^2 = 98.07\%$).
        5. **Segment Product Archetypes:** Uncover market clusters using unsupervised K-Means clustering.
        """)

    with col_right:
        st.subheader("🏆 Key Findings Summary")
        st.markdown("""
        - **Heavy Right Skew:** 50% of catalog items sell below **₹550**, while high-end outliers reach **₹571,230**.
        - **Deep Discount Culture:** **45.85%** of products receive discounts $\ge 50\%$; median discount is **45.0%**.
        - **Zero Rating Penalty:** Product rating exhibits virtually zero correlation with discount depth ($r = -0.002$).
        - **Ensemble Dominance:** Gradient Boosting predicts selling prices with an $R^2$ of **0.9807** and MAE of **₹290.21**.
        """)

    st.divider()
    st.subheader("📊 Top Catalog Categories Distribution")
    top_cats = df["primary_category"].value_counts().head(8).reset_index()
    top_cats.columns = ["Category", "Product Count"]
    fig = px.bar(
        top_cats,
        x="Product Count",
        y="Category",
        orientation="h",
        color="Product Count",
        color_continuous_scale="Blues",
        text="Product Count"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), template="plotly_white", height=380, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 2: DATA OVERVIEW & DICTIONARY
# -----------------------------------------------------------------------------
elif menu_choice == "📋 Data Overview & Dictionary":
    st.markdown('<div class="main-header">Dataset Overview & Schema Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Inspecting data dimensions, missing value resolutions, and data dictionary</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔍 Interactive Data Browser", "📖 Data Dictionary", "🧹 Cleaning & Quality Audit"])

    with tab1:
        st.subheader("Filtered Data Preview")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            sel_cat = st.selectbox("Filter Category", ["All"] + sorted(df["primary_category"].unique().tolist()))
        with c2:
            sel_tier = st.selectbox("Filter Price Tier", ["All"] + sorted(df["price_tier"].dropna().unique().tolist()))
        with c3:
            search_name = st.text_input("Search Product Title", "")

        view_df = df.copy()
        if sel_cat != "All":
            view_df = view_df[view_df["primary_category"] == sel_cat]
        if sel_tier != "All":
            view_df = view_df[view_df["price_tier"] == sel_tier]
        if search_name:
            view_df = view_df[view_df["product_name"].str.contains(search_name, case=False, na=False)]

        st.caption(f"Showing {len(view_df):,} matching products")
        display_cols = [
            "product_name", "primary_category", "brand", "retail_price",
            "discounted_price", "discount_percentage", "discount_tier", "rating_score"
        ]
        st.dataframe(view_df[display_cols].head(200), use_container_width=True, height=450)
        
        csv_data = view_df[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered CSV", csv_data, "flipkart_filtered_sample.csv", "text/csv")

    with tab2:
        st.subheader("Data Dictionary (31 Attributes)")
        data_dict = pd.DataFrame([
            {"Column": "uniq_id", "Type": "string", "Description": "Unique identifier for each product listing"},
            {"Column": "product_name", "Type": "string", "Description": "Full title and specification summary of the product"},
            {"Column": "primary_category", "Type": "string", "Description": "Top-level category extracted from category tree"},
            {"Column": "sub_category", "Type": "string", "Description": "Second-level category taxonomy branch"},
            {"Column": "brand", "Type": "string", "Description": "Manufacturer / Brand name (Unbranded items preserved)"},
            {"Column": "retail_price", "Type": "float64", "Description": "Original Maximum Retail Price (MRP) in INR"},
            {"Column": "discounted_price", "Type": "float64", "Description": "Actual selling price listed on Flipkart in INR"},
            {"Column": "discount_percentage", "Type": "float64", "Description": "Calculated percentage savings: ((MRP - Selling)/MRP)*100"},
            {"Column": "discount_tier", "Type": "category", "Description": "Binned markdown bracket (No Discount, Low, Moderate, High, Clearance)"},
            {"Column": "price_tier", "Type": "category", "Description": "Binned MRP brackets (Budget, Economy, Mid-Range, Premium, Luxury)"},
            {"Column": "rating_score", "Type": "float64", "Description": "Numeric customer rating (1.0 to 5.0 stars, NaN if unrated)"},
            {"Column": "is_rated", "Type": "int64", "Description": "Binary flag (1 = product has ratings, 0 = unrated)"},
            {"Column": "is_FK_Advantage_product", "Type": "bool", "Description": "Flipkart Assured / Advantage seller certification badge"},
            {"Column": "cluster_persona", "Type": "string", "Description": "K-Means assigned market pricing segment archetype"}
        ])
        st.dataframe(data_dict, use_container_width=True)

    with tab3:
        st.subheader("Data Quality & Cleaning Reconciliation")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            **Raw vs Clean Reconciliation:**
            - **Raw Rows:** 20,000 | **Processed Rows:** 19,922
            - **Invalid Price Rows Dropped:** 78 rows (0.39%)
            - **Missing Brand Reconciliation:** 5,864 raw missing - 13 dropped = 5,851 `"Unbranded / Generic"`.
            - **Rated Products Reconciliation:** 1,849 raw rated - 10 dropped = 1,839 rated products preserved.
            """)
        with col_b:
            null_summary = pd.DataFrame({
                "Metric": ["Retail Price Nulls", "Discounted Price Nulls", "Primary Category Nulls", "Rating Nulls (Unrated)"],
                "Clean Dataset Count": [0, 0, 0, 18083],
                "Percent of Catalog": ["0.0%", "0.0%", "0.0%", "90.77%"]
            })
            st.dataframe(null_summary, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 3: PRICE ANALYSIS
# -----------------------------------------------------------------------------
elif menu_choice == "💰 Price Analysis":
    st.markdown('<div class="main-header">Price Distribution & Parity Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Exploring MRP benchmarks, selling price dynamics, and category variations</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Retail Price vs Discounted Selling Price")
        sample_size = st.slider("Sample Points for Scatter Plot", 1000, 8000, 3000, step=1000)
        p_sample = df.sample(n=sample_size, random_state=42)
        
        fig_scatter = px.scatter(
            p_sample,
            x="retail_price",
            y="discounted_price",
            color="price_tier",
            hover_data=["product_name", "primary_category", "discount_percentage"],
            labels={"retail_price": "Retail Price / MRP (₹)", "discounted_price": "Selling Price (₹)"},
            log_x=True,
            log_y=True,
            template="plotly_white"
        )
        fig_scatter.add_trace(go.Scatter(
            x=[35, 600000],
            y=[35, 600000],
            mode="lines",
            name="Parity Line (0% Off)",
            line=dict(color="red", dash="dash", width=2)
        ))
        fig_scatter.update_layout(height=480)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("Points on the red parity line represent products sold at 0% discount (full MRP).")

    with c2:
        st.subheader("Price Distribution (Histogram)")
        use_log = st.checkbox("Apply Log Scale (Normalizes Extreme Outliers)", value=True)
        
        if use_log:
            fig_hist = px.histogram(
                df,
                x="log_discounted_price",
                nbins=40,
                color_discrete_sequence=["#2874f0"],
                labels={"log_discounted_price": "Log1p(Selling Price)"},
                marginal="box",
                template="plotly_white"
            )
            fig_hist.update_layout(title="Log-Transformed Selling Price Distribution", height=480)
        else:
            p95 = df["discounted_price"].quantile(0.95)
            fig_hist = px.histogram(
                df[df["discounted_price"] <= p95],
                x="discounted_price",
                nbins=40,
                color_discrete_sequence=["#2874f0"],
                labels={"discounted_price": "Selling Price (₹)"},
                marginal="box",
                template="plotly_white"
            )
            fig_hist.update_layout(title=f"Raw Selling Price Distribution (Capped at 95th Pct: ₹{p95:,.0f})", height=480)
        st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()
    st.subheader("Category-Wise Price Comparison")
    top_cats = df["primary_category"].value_counts().head(10).index
    cat_prices = df[df["primary_category"].isin(top_cats)].groupby("primary_category")[["retail_price", "discounted_price"]].median().reset_index()
    cat_prices = cat_prices.sort_values(by="discounted_price", ascending=False)
    
    fig_cat = go.Figure(data=[
        go.Bar(name='Median MRP', x=cat_prices['primary_category'], y=cat_prices['retail_price'], marker_color='#93c5fd'),
        go.Bar(name='Median Selling Price', x=cat_prices['primary_category'], y=cat_prices['discounted_price'], marker_color='#2874f0')
    ])
    fig_cat.update_layout(barmode='group', template="plotly_white", height=400, yaxis_title="Price (₹ INR)")
    st.plotly_chart(fig_cat, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 4: DISCOUNT ANALYSIS
# -----------------------------------------------------------------------------
elif menu_choice == "🏷️ Discount Analysis":
    st.markdown('<div class="main-header">Discount Strategy & Markdown Depth</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating discount percentage distributions, promotional tiers, and category elasticity</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Discount Percentage Distribution")
        fig_disc_hist = px.histogram(
            df,
            x="discount_percentage",
            nbins=40,
            color_discrete_sequence=["#f97316"],
            marginal="box",
            labels={"discount_percentage": "Discount (%)"},
            template="plotly_white"
        )
        fig_disc_hist.add_vline(x=df["discount_percentage"].median(), line_dash="dash", line_color="blue", annotation_text=f"Median: {df['discount_percentage'].median():.1f}%")
        fig_disc_hist.update_layout(height=420)
        st.plotly_chart(fig_disc_hist, use_container_width=True)

    with c2:
        st.subheader("Breakdown by Discount Tier")
        tier_counts = df["discount_tier"].value_counts().reset_index()
        tier_counts.columns = ["Discount Tier", "Count"]
        fig_tier = px.pie(
            tier_counts,
            names="Discount Tier",
            values="Count",
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            hole=0.45,
            template="plotly_white"
        )
        fig_tier.update_layout(height=420)
        st.plotly_chart(fig_tier, use_container_width=True)

    st.divider()
    st.subheader("Highest and Lowest Discount Categories")
    col_high, col_low = st.columns(2)
    
    top_15_cats = df["primary_category"].value_counts().head(15).index
    agg_disc = df[df["primary_category"].isin(top_15_cats)].groupby("primary_category")["discount_percentage"].median().sort_values(ascending=False).reset_index()
    agg_disc.columns = ["Category", "Median Discount (%)"]

    with col_high:
        st.markdown("**Top 5 Steepest Discount Categories:**")
        st.dataframe(agg_disc.head(5).style.format({"Median Discount (%)": "{:.1f}%"}), use_container_width=True)
        st.caption("Categories like Automotive and Mobile Accessories rely on aggressive ~55-60% markdowns.")

    with col_low:
        st.markdown("**Top 5 Lowest Discount Categories:**")
        st.dataframe(agg_disc.tail(5).sort_values("Median Discount (%)").style.format({"Median Discount (%)": "{:.1f}%"}), use_container_width=True)
        st.caption("Personal Care and Footwear maintain strict price integrity (~14-40% discount).")


# -----------------------------------------------------------------------------
# PAGE 5: RATING ANALYSIS
# -----------------------------------------------------------------------------
elif menu_choice == "⭐ Rating Analysis":
    st.markdown('<div class="main-header">Customer Rating Analysis & Reputation Dynamics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Investigating rating distributions and correlation with price and discounts</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Catalog Rating Completeness")
        rated_pie = pd.DataFrame({
            "Status": ["Unrated Products", "Rated Products"],
            "Count": [len(df) - df["is_rated"].sum(), df["is_rated"].sum()]
        })
        fig_rated_pie = px.pie(
            rated_pie,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map={"Unrated Products": "#cbd5e1", "Rated Products": "#8b5cf6"},
            hole=0.5,
            template="plotly_white"
        )
        fig_rated_pie.update_layout(height=380)
        st.plotly_chart(fig_rated_pie, use_container_width=True)

    with c2:
        st.subheader("Rating Score Distribution (1.0 to 5.0 Stars)")
        rated_df = df[df["is_rated"] == 1]
        fig_rating_hist = px.histogram(
            rated_df,
            x="rating_score",
            nbins=15,
            color_discrete_sequence=["#8b5cf6"],
            labels={"rating_score": "Star Rating"},
            template="plotly_white"
        )
        fig_rating_hist.add_vline(x=rated_df["rating_score"].median(), line_dash="dash", line_color="red", annotation_text=f"Median: {rated_df['rating_score'].median():.1f}★")
        fig_rating_hist.update_layout(height=380)
        st.plotly_chart(fig_rating_hist, use_container_width=True)

    st.divider()
    st.subheader("Do Customer Ratings Correlate with Discounts?")
    
    rated_df = rated_df.copy()
    rated_df["Rating Bucket"] = pd.cut(
        rated_df["rating_score"],
        bins=[0.9, 2.0, 3.0, 4.0, 5.0],
        labels=["1★ to 2★", "2★ to 3★", "3★ to 4★", "4★ to 5★"]
    )
    
    fig_rating_box = px.box(
        rated_df.dropna(subset=["Rating Bucket"]),
        x="Rating Bucket",
        y="discount_percentage",
        color="Rating Bucket",
        color_discrete_sequence=px.colors.sequential.Purples_r,
        labels={"discount_percentage": "Discount (%)"},
        template="plotly_white"
    )
    fig_rating_box.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_rating_box, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <b>Empirical Statistical Proof:</b> The Pearson correlation between star rating and discount percentage is <b>r = -0.0020</b>. 
        Customer satisfaction scores remain consistently high (~3.8★ to 4.0★) regardless of whether an item has zero discount or is marked down by 75%.
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# PAGE 6: MACHINE LEARNING & PREDICTION
# -----------------------------------------------------------------------------
elif menu_choice == "🤖 Machine Learning & Prediction":
    st.markdown('<div class="main-header">Predictive Modeling & Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating supervised models and live price estimation without feature leakage</div>', unsafe_allow_html=True)

    tab_ml1, tab_ml2 = st.tabs(["🎯 Supervised Price Predictor", "🧩 K-Means Market Segmentation"])

    with tab_ml1:
        st.subheader("1. Supervised Models Benchmark")
        ml_comparison = pd.DataFrame([
            {"Model Architecture": "Simple Baseline (Median)", "MAE (₹)": "₹1,601.09", "RMSE (₹)": "₹6,205.38", "R² Score": "-0.0536", "Rank": "Baseline"},
            {"Model Architecture": "Ridge Regression (Linear)", "MAE (₹)": "₹444.61", "RMSE (₹)": "₹1,163.12", "R² Score": "0.9630", "Rank": "3rd"},
            {"Model Architecture": "Random Forest Regressor", "MAE (₹)": "₹267.11", "RMSE (₹)": "₹884.70", "R² Score": "0.9786", "Rank": "2nd"},
            {"Model Architecture": "Gradient Boosting Regressor", "MAE (₹)": "₹290.21", "RMSE (₹)": "₹838.82", "R² Score": "0.9807", "Rank": "🏆 Best"}
        ])
        st.table(ml_comparison)

        st.divider()
        st.subheader("2. Interactive Selling Price Predictor (Live Model Inference)")
        st.caption("Enter product attributes to estimate expected discounted selling price using the trained Gradient Boosting model:")

        if ml_artifacts is not None:
            c1, c2, c3 = st.columns(3)
            with c1:
                inp_mrp = st.number_input("Retail Price / MRP (₹ INR)", min_value=50.0, max_value=200000.0, value=1999.0, step=50.0)
                inp_cat = st.selectbox("Product Category", ml_artifacts["top_categories"])
            with c2:
                inp_brand = st.selectbox("Brand Name", ["Unbranded / Generic"] + ml_artifacts["top_brands"])
                inp_words = st.slider("Product Name Word Count", 2, 20, 6)
            with c3:
                inp_desc_len = st.slider("Description Word Count", 10, 300, 75)
                inp_fka = st.checkbox("Flipkart Advantage / Assured Product", value=False)
                inp_rated = st.checkbox("Product Has Customer Rating", value=True)

            if st.button("🔮 Calculate Predicted Selling Price", type="primary"):
                input_df = pd.DataFrame([{
                    "retail_price": inp_mrp,
                    "product_name_word_count": inp_words,
                    "description_word_count": inp_desc_len,
                    "is_FK_Advantage_product": int(inp_fka),
                    "is_rated": int(inp_rated),
                    "primary_category": inp_cat,
                    "brand": inp_brand
                }])

                proc_input = ml_artifacts["preprocessor"].transform(input_df)
                pred_price = float(ml_artifacts["model"].predict(proc_input)[0])
                pred_price = max(1.0, min(pred_price, inp_mrp))  # Bounded
                pred_discount = max(0.0, ((inp_mrp - pred_price) / inp_mrp) * 100)
                savings = inp_mrp - pred_price

                p1, p2, p3 = st.columns(3)
                p1.metric("Predicted Selling Price", f"₹{pred_price:,.2f}")
                p2.metric("Estimated Discount", f"{pred_discount:.1f}%")
                p3.metric("Customer Savings", f"₹{savings:,.2f}")
        else:
            st.warning("Model artifact not found. Please verify models/saved/price_model_artifacts.joblib.")

    with tab_ml2:
        st.subheader("Unsupervised Market Pricing Clusters (K-Means)")
        
        cluster_data = pd.DataFrame([
            {"Segment": "Segment 1: Mass-Market Deep Discount", "Catalog %": "43.0%", "Median MRP": "₹999", "Median Selling": "₹399", "Median Discount": "57.2%", "Core Profile": "High volume, fast-fashion & phone accessories"},
            {"Segment": "Segment 2: Mid-Range Moderate Discount", "Catalog %": "24.8%", "Median MRP": "₹2,450", "Median Selling": "₹1,299", "Median Discount": "45.5%", "Core Profile": "Balanced branded apparel, automotive & home decor"},
            {"Segment": "Segment 3: Premium / Luxury Niche", "Catalog %": "5.5%", "Median MRP": "₹32,002", "Median Selling": "₹24,112", "Median Discount": "23.1%", "Core Profile": "High-value fine jewellery, watches & consumer tech"},
            {"Segment": "Segment 4: Low-Discount Essentials", "Catalog %": "26.7%", "Median MRP": "₹599", "Median Selling": "₹499", "Median Discount": "10.3%", "Core Profile": "Low ticket staples, personal care & full-MRP items"}
        ])
        st.table(cluster_data)

        if "cluster_persona" in df.columns:
            st.divider()
            st.subheader("Explore Products by Cluster")
            sel_cluster = st.selectbox("Select Segment to Inspect", df["cluster_persona"].dropna().unique().tolist())
            cluster_subset = df[df["cluster_persona"] == sel_cluster][["product_name", "primary_category", "retail_price", "discounted_price", "discount_percentage"]].head(100)
            st.dataframe(cluster_subset, use_container_width=True)


# -----------------------------------------------------------------------------
# PAGE 7: INSIGHTS & CONCLUSION
# -----------------------------------------------------------------------------
elif menu_choice == "💡 Insights & Conclusion":
    st.markdown('<div class="main-header">Strategic Insights & Final Conclusions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Synthesis of empirical findings, commercial takeaways, and academic conclusions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 Strategic E-Commerce Takeaways")
        st.markdown("""
        1. **The ₹999 Anchor Phenomenon:**
           The single most common retail anchor price across apparel and jewellery is **₹999**, typically discounted to **₹499** (~50% off). Retailers deliberately use four-digit thresholds to maximize perceived promotional value.
           
        2. **Category Margin Disparities:**
           Discount strategies are highly siloed by vertical. Categories with high inventory turnover (Automotive Accessories, Mobile Cases) afford steep 60%+ discounts, whereas Personal Care and Footwear maintain strict 14-40% bands.
           
        3. **Reputation Invariance:**
           Contrary to classical retail theory, severe discounting on Flipkart does **not** degrade consumer rating sentiment ($r = -0.002$). E-commerce consumers welcome clearance markdowns without associating lower prices with defective quality.
        """)

    with col2:
        st.subheader("⚠️ Project Scope & Limitations")
        st.markdown("""
        1. **Cross-Sectional Catalog Snapshot:**
           The dataset represents a discrete web crawl period. Longitudinal price elasticity over festival sales (e.g., Big Billion Days) requires continuous daily historical scraping.
           
        2. **Seller Identity Anonymity:**
           Individual merchant ratings and multi-seller Buy Box competitions are not captured in the raw schema.
           
        3. **Rating Sparsity:**
           Only **9.23%** of products carry explicit ratings, reflecting the typical long-tail distribution of unrated items in e-commerce catalogs.
        """)

    st.divider()
    st.subheader("🏁 Academic Project Conclusion")
    st.markdown("""
    This project successfully designed, implemented, and validated a complete **Data Analytics and Predictive Intelligence pipeline** on genuine Flipkart product data:
    - Ingested and cleaned **19,922 records** without data distortion.
    - Derived actionable business intelligence across price elasticity, markdown tiers, and brand power.
    - Built a high-performance **Gradient Boosting Regressor** achieving **$R^2 = 0.9807$** and **MAE = ₹290.21** without data leakage.
    - Clustered product inventory into **4 actionable strategic market segments** via K-Means.
    - Deployed a production-ready, interactive Streamlit analytics dashboard.
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2026 B.Tech Data Analytics Project | Flipkart Price Analysis")
