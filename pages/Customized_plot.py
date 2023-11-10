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

# Format preparation
df['date'] = pd.to_datetime(df['date'])
df['release_date'] = pd.to_datetime(df['release_date'])
df = df[df['avg_peak_perc']!='NaN%']
df = df.dropna()

# Header
st.header("👋")
st.title("Customized Plot")

##### Filter #####

# Featuer for x axis

features = ['avg', 'gain', 'peak', 'avg_peak_perc']
order_bool = st.toggle(label='Ascending')
y = st.selectbox("Select a Feature", features)
# left_col, right_col = st.columns(2)
# with right_col: y = st.selectbox("Select a Feature", features)
# with left_col: order_bool = st.toggle(label='Ascending')

order='Worst' if order_bool else 'Highest'
y_name = y.replace('_', ' ').title()

# Data - sorting
gb = df[['gamename', 'date', y]].sort_values(by=y, ascending=order_bool).reset_index()
top_games = gb.gamename.unique()[0:5]

# Data Frame
title = f"1.1 Dataset Sorted by :blue[{y_name}]:"
st.subheader(title)
st.dataframe(gb)

title = f"1.2 Five Games with the {order} Monthly :blue[{y_name}]:"
st.subheader(title)
st.write(top_games)

# Plot 1 - markdown
st.markdown(
    """
    ***
    ## 2.0 Customized Plot
    """
)

# Plot 1 Multiselect box
options = top_games
selected_options = st.multiselect('Select Video Games', options)

# Plot 1
selected_names = ','.join(selected_options)
title = f"Monthly :blue[{y_name}] of {selected_names} Over Time"
st.write(title)

gb2 = gb.sort_values(by='date')
gb_list = {game: gb2[gb2["gamename"] == game] for game in selected_options}


fig = go.Figure()
# fig.update_layout(title=title)
fig.update_layout(
    xaxis_title='Date',
    yaxis_title=y_name,
)
for game, gb2 in gb_list.items():
    fig = fig.add_trace(go.Scatter(x=gb2["date"], y=gb2[y], name=game, mode='lines'))
st.plotly_chart(fig)