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
st.title("Games with Highest Player Monthly Average")

# Markdown
# Plot 1 - selecting individual game of highest gain
st.markdown(
    """
    ## 1.0 Individual Game
    This is a plot of average player count over time, as well as an implementation of Ploty "selectbox". Here is our data sorted by 'avg' in descending order. 
    """
)

# Data
st.markdown(
    """
    &nbsp;  
    ##### Record of games earned highest average player count within a month
    """
)
gb = df[['gamename', 'date', 'avg']].sort_values(by='avg', ascending=False).reset_index()
top_avg_games = gb.gamename.unique()[0:5]
st.dataframe(gb)

st.markdown("""***""")


# Plot 1 Select box
options = top_avg_games
selected_option = st.selectbox("Select a Video Game", options)

# Plot 1
gb1 = gb[gb['gamename']==selected_option].sort_values(by='date').reset_index()
title = f"Monthly Average Player Count of {selected_option} Over Time:"
fig = px.line(gb1, x='date', y='avg', title=title)
st.plotly_chart(fig, use_container_width=True)


# Plot 2 markdown
st.markdown(
    """
    ***
    ## 2.0 Comparison 
    """
)

# Plot 2 Multiselect box
options = top_avg_games
selected_options = st.multiselect('Select Video Games', options)

# Plot 2
title = "Monthly Average Player Count of {} Over Time".format(", ".join(selected_options))
gb2 = gb.sort_values(by='date')
gb_list = {game: gb2[gb2["gamename"] == game] for game in selected_options}

fig = go.Figure()
fig.update_layout(title=title)
for game, gb2 in gb_list.items():
    fig = fig.add_trace(go.Scatter(x=gb2["date"], y=gb2["avg"], name=game, mode='lines'))
st.plotly_chart(fig)