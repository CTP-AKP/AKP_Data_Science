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
df['avg_peak_perc'] = df['avg_peak_perc'].str.rstrip('%').astype('float') 
df = df.dropna()

# Header
st.header("👋")
st.title("Customized Plot on :blue[General Features]")

##### FILTER #####
# Featuer for both axis
features = ['avg', 'gain', 'peak', 'avg_peak_perc']
genres = features

left_col, right_col = st.columns(2)
order = st.toggle(label='Find the Worst Games', value=False)        # descending order toggle switch
y = st.selectbox("Select a Feature", features)                      # feature select box
order_name='Worst' if order else 'Highest'                          # string formating
y_name = y.replace('_', ' ').title()

# Data - sorting and filtering
df_ax = df[['gamename', 'date', y]].sort_values(by=y, ascending=order).reset_index()    # Data - Plot 1
top_games = df_ax.gamename.unique()[0:5]
df_bx = df[['gamename', 'date']+features].sort_values(by=y, ascending=order).reset_index()      # Data - Plot 2

# Dataframe preview
title = f"1.1 Dataset of Games Sorted by :blue[{y_name}]:"
st.subheader(title)
st.dataframe(df_ax)

title = f"1.2 Five Games with the Overall :red[{order_name}] Monthly :blue[{y_name}]:"
st.subheader(title)
st.write(top_games)



##### PLOT 1 #####
# Plot 1 - markdown
st.markdown("""***""")
title = f"1.3 Games with the Overall :red[{order_name}] :blue[{y_name}]"
st.subheader(title)

# Plot 1 - select box
options = top_games
selected_options = st.multiselect('Select Video Games', options)

# Plot 1
title_names = ','.join(selected_options)
plot_title = f"Monthly {y_name} of {title_names} Over Time"
gb = df_ax.sort_values(by='date')
gb_list = {game: gb[gb["gamename"] == game] for game in selected_options}

fig_1 = go.Figure()
fig_1.update_layout(
    title = plot_title, 
    xaxis_title = 'Date',
    yaxis_title = y_name,
)
for game, gb in gb_list.items():
    fig_1 = fig_1.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=game, mode='lines'))
st.plotly_chart(fig_1)


