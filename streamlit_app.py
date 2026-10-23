import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Delivery Analytics Dashboard")
st.caption("Data-Driven Business Insights")

# Connect to MySQL database
connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Uwais@2012", 
        database="food_delivery_analysis"
    )

    df = pd.read_sql("SELECT * FROM food_orders", connection)

except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

finally:
    if connection is not None and connection.is_connected():
        connection.close()

# Prepare numeric columns
for column in [
    "Final_Amount",
    "Delivery_Time_Min",
    "Delivery_Rating",
    "Profit_Margin_Percentage"
]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Calculate KPIs
total_orders = len(df)
total_revenue = df["Final_Amount"].sum()
average_order_value = df["Final_Amount"].mean()

delivered = df[df["Order_Status"] == "Delivered"]
average_delivery_time = delivered["Delivery_Time_Min"].mean()
average_delivery_rating = delivered["Delivery_Rating"].mean()

cancellation_rate = (
    (df["Order_Status"] == "Cancelled").mean() * 100
)

profit_margin = df["Profit_Margin_Percentage"].mean()

# Display KPI cards
st.subheader("📊 Key Performance Indicators")

row1 = st.columns(4)
row1[0].metric("Total Orders", f"{total_orders:,}")
row1[1].metric("Total Revenue", f"₹{total_revenue:,.0f}")
row1[2].metric(
    "Average Order Value",
    f"₹{average_order_value:,.2f}"
    if pd.notna(average_order_value) else "N/A"
)
row1[3].metric(
    "Average Delivery Time",
    f"{average_delivery_time:.1f} min"
    if pd.notna(average_delivery_time) else "N/A"
)

row2 = st.columns(3)
row2[0].metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
row2[1].metric(
    "Average Delivery Rating",
    f"{average_delivery_rating:.2f} / 5"
    if pd.notna(average_delivery_rating) else "N/A"
)
row2[2].metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
    if pd.notna(profit_margin) else "N/A"
)

st.success(f"Connected to MySQL — {total_orders:,} orders loaded.")