import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.title("Mario Kart and how Popular Mario Games Are")

# Load the data
df = pd.read_csv('..\data/Video_Games.csv')
df.drop_duplicates(inplace=True)
df.dropna(subset=['Global_Sales'], inplace=True)  # Remove rows with NULL sales

# Filter out Mario Kart games
mario_kart_df = df[df['Name'].str.contains("Mario Kart", na=False)].groupby("Name")["Global_Sales"].sum().sort_values()

st.subheader("Popularity of Mario Kart Games by Sales:")
st.markdown("""
            The bar chart below reveals the popularity of various Mario Kart games based on their global sales.
            Sales are an excellent metric to understand the popularity of a game, indicating both its reach and reception among gamers.
            """)

# Show data table for Mario Kart games
st.write(mario_kart_df)

## Create Altair chart
chart = alt.Chart(mario_kart_df.reset_index()).mark_bar().encode(
    y=alt.Y('Name:N', sort='-x'),
    x=alt.X('Global_Sales:Q', title='Global Sales In Millions')  # Updated the title here
).properties(
    width=600,
    height=400
)

st.altair_chart(chart)

# Aggregate Sales for all Mario games vs all GTA games
gta_sales = df[df['Name'].str.contains("Grand Theft Auto", na=False)]['Global_Sales'].sum()
mario_sales = df[df['Name'].str.contains("Mario", na=False)]['Global_Sales'].sum()

# Displaying the table
sales_df = pd.DataFrame({
    'Game Franchise': ['Mario Games', 'GTA Games'],
    'Global Sales': [mario_sales, gta_sales]
})
st.write(sales_df)

st.subheader("Total Sales of all Mario games vs all GTA games:")
st.markdown("""
            The bar chart below provides a comparative visualization of total sales from all Mario games against all Grand Theft Auto (GTA) games. 
            The immense popularity of these franchises offers an intriguing perspective on their impact in the gaming industry.
            """)

# Display the sales data using Streamlit's built-in bar chart
st.bar_chart(sales_df.set_index('Game Franchise'))