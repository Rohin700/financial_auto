# python3 -m pip install streamlit pandas mysql-connector-python plotly 
# for importing this library
# to run this file run 'streamlit run app.py' on terminal
    
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
load_dotenv()

st.markdown(
    """
    <style>
    /* Hide Streamlit menu (top-right three dots) */
    #MainMenu {visibility: hidden;}

    /* Hide Streamlit footer (Deploy button / footer) */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
# Update with your MySQL credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# ---------------------------
# FETCH DATA FUNCTION
# ---------------------------
@st.cache_data
def fetch_data():
    query = "SELECT * FROM sales_data"
    df = pd.read_sql(query, engine)
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Convert numeric columns to proper types
    numeric_cols = ['revenue', 'mean', 'orders']  # adjust based on your DB
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill NaN with 0
    df.fillna(0, inplace=True)
    
    return df

# ---------------------------
# LOAD DATA
# ---------------------------
df = fetch_data()

# ---------------------------
# DASHBOARD TITLE
# ---------------------------
st.markdown("<h1 style='text-align:center; color:#032B44;'>📊 Financial Analytics Dashboard</h1>", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filter DataFrame
df_filtered = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date)) &
    (df['category'].isin(category_filter))
]

# ---------------------------
# KPI CARDS
# ---------------------------
total_revenue = df_filtered['revenue'].sum()
total_orders = len(df_filtered)
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
top_category = df_filtered.groupby('category')['revenue'].sum().idxmax() if len(df_filtered) > 0 else "N/A"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")

with col2:
    st.metric(label="Total Orders", value=total_orders)

with col3:
    st.metric(label="Avg Order Value", value=f"₹{avg_order_value:,.2f}")

with col4:
    st.metric(label="Top Category", value=top_category)

# ---------------------------
# CHARTS
# ---------------------------

# Revenue Trend Line Chart
rev_trend = df_filtered.groupby('date')['revenue'].sum().reset_index()
fig1 = px.line(rev_trend, x='date', y='revenue', title="Daily Revenue Trend", markers=True)
st.plotly_chart(fig1, width='stretch')

# Category Revenue Bar Chart
cat_rev = df_filtered.groupby('category')['revenue'].sum().reset_index()
fig2 = px.bar(cat_rev, x='category', y='revenue', title="Revenue by Category", color='category')
st.plotly_chart(fig2, width='stretch')

# Top Products Chart
if 'product' in df_filtered.columns:
    top_products = df_filtered.groupby('product')['revenue'].sum().nlargest(5).reset_index()
    fig3 = px.bar(top_products, x='revenue', y='product', title="Top 5 Products", orientation='h')
    st.plotly_chart(fig3, width='stretch')

# ---------------------------
# DATA TABLE (optional)
# ---------------------------
st.header("Filtered Data Table")
st.dataframe(df_filtered)
