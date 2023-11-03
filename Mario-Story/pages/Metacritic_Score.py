import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Set the title of the web app
st.title("Game Statistics Visualization")

# Load the dataset
df = pd.read_pickle('../data/pk-games.pk1')

# Clean and prepare the dataset
# Convert Metacritic score to numeric and handle possible errors
df['Metacritic score'] = pd.to_numeric(df['Metacritic score'], errors='coerce')

# Drop rows where Metacritic score or Release date is NaN (not a number)
df = df.dropna(subset=['Metacritic score', 'Release date'])

# Convert Release date to datetime
df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce', infer_datetime_format=True)

# Drop rows where Release date is still NaT (not a time) after conversion
df = df.dropna(subset=['Release date'])

# User input for Metacritic score range
min_score, max_score = st.slider(
    'Select Metacritic Score Range', 
    int(df['Metacritic score'].min()), 
    int(df['Metacritic score'].max()), 
    (50, 100)
)

# Filter the dataframe based on the selected Metacritic score range
filtered_df = df[(df['Metacritic score'] >= min_score) & (df['Metacritic score'] <= max_score)]

# Display the filtered dataframe
st.dataframe(filtered_df[['Name', 'Metacritic score', 'Release date', 'Peak CCU', 'Price']])

# Explanatory entry about the relationship between Metacritic score and CCU
st.markdown("""
    ## Metacritic Score and Concurrent Users (CCU)
    A game's Metacritic score often reflects its critical reception, which can influence the number of concurrent users. 
    Higher scores might correlate with more users playing the game simultaneously, indicating its popularity and quality.
""")

# Scatter plot for Metacritic score vs CCU
scatter_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X('Metacritic score', scale=alt.Scale(zero=False)),
    y=alt.Y('Peak CCU', scale=alt.Scale(zero=False)),
    tooltip=['Name', 'Metacritic score', 'Peak CCU']
).interactive()
st.altair_chart(scatter_chart, use_container_width=True)

# Explanatory entry about the relationship between Metacritic score and Price
st.markdown("""
    ## Metacritic Score and Price
    Intuitively, one might assume that higher-rated games are priced higher. However, this isn't always the case. 
    Various factors, including genre, developer reputation, and marketing, can affect a game's pricing strategy.
    Note: Free games (Price = 0) are excluded from this analysis.
""")

# Filter out games with a price of 0
price_filtered_df = filtered_df[filtered_df['Price'] > 0]

# Scatter plot for Metacritic score vs Price
price_chart = alt.Chart(price_filtered_df).mark_circle(size=60).encode(
    x=alt.X('Metacritic score', scale=alt.Scale(zero=False)),
    y=alt.Y('Price', scale=alt.Scale(zero=False)),
    tooltip=['Name', 'Metacritic score', 'Price']
).interactive()
st.altair_chart(price_chart, use_container_width=True)