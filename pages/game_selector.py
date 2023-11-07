# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
sns.set()

# Load the dataset
df = pd.read_csv('./data/join_02.csv')

# date format preparation
df['date'] = pd.to_datetime(df['date'])
df['release_date'] = pd.to_datetime(df['release_date'])

# Title
st.header("👋")
st.title("Video Game Lifespan in Relation to Other Features")


st.markdown(
    """
    How different factors affect the lifespan of a video game
    """
)

gb = df[['gamename', 'date', 'gain']].sort_values(by='gain', ascending=True).reset_index()
top_gained_games = gb.head().gamename.to_list()

options = top_gained_games
selected_option = st.selectbox("Select a Most-gained Video Game", options)
gb = gb[gb['gamename']==selected_option].sort_values(by='date').reset_index()

inform = f"{selected_option} Chart:"
fig = px.line(gb, x='date', y='gain', title=inform)

st.plotly_chart(fig, use_container_width=True)