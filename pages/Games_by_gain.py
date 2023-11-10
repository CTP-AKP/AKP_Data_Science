# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

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
st.title("Plotly Test | Games with Highest Player Gain")

# Markdown
# Plot 1 - selecting individual game of highest gain
st.markdown(
    """
    ## 1.0 Individual Game
    This is a plot of gain over time, as well as an implementation of Ploty "selectbox". Here is our data sorted by gain in descending order. 
    ```
    selection = st.selectbox("Description", options)
    selection = st.multiselect("Description", options)
    ```
    """
)

# Data
st.markdown(
    """
    &nbsp;  
    ##### Game earned highest gain within a month
    """
)
gb = df[['gamename', 'date', 'gain']].sort_values(by='gain', ascending=True).reset_index()
top_gained_games = gb.head().gamename.to_list()
st.dataframe(gb.head())
st.markdown("""***""")


# Plot 1 Select box
options = top_gained_games
selected_option = st.selectbox("Select a Video Game", options)

# Plot 1
gb1 = gb[gb['gamename']==selected_option].sort_values(by='date').reset_index()
title = f"Monthly Player Gain of {selected_option} Over Time:"
fig = px.line(gb1, x='date', y='gain', title=title)
st.plotly_chart(fig, use_container_width=True)


# Plot 2 markdown
st.markdown(
    """
    ***
    ## 2.0 Comparison 
    """
)

# Plot 2 Multiselect box
options = top_gained_games
selected_options = st.multiselect('Select Video Games', options)

# Plot 2
title = "Monthly Player Gain of {} Over Time".format(", ".join(selected_options))
# st.header("You selected: {}".format(", ".join(selected_options)))
gb_list = {game: df[df["gamename"] == game] for game in selected_options}

fig = go.Figure()
fig.update_layout(title=title)
for game, df in gb_list.items():
    fig = fig.add_trace(go.Scatter(x=df["date"], y=df["gain"], name=game, mode='lines'))
st.plotly_chart(fig)