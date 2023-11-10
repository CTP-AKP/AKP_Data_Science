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
st.title("Customized Plot on Category")

##### FILTER #####
# Featuer for both axis
features = ['avg', 'gain', 'peak', 'avg_peak_perc']
genres = ['multi_player', 'pvp', 'co-op']

left_col, right_col = st.columns(2)
order_bool = st.toggle(label='Find the Worst Games', value=False)   # descending order toggle switch
with left_col: y = st.selectbox("Select a Feature", features)       # feature select box
with right_col: ax = st.selectbox("Select a Category", genres)     # category select box
order='Worst' if order_bool else 'Highest'                          # string formating
y_name = y.replace('_', ' ').title()

# Data - sorting and filtering
df_ax = df[df[ax]==1]
df_ax = df_ax[['gamename', 'date', y, ax]].sort_values(by=y, ascending=order_bool).reset_index()    # Data - Plot 1
top_games = df_ax.gamename.unique()[0:5]
df_bx = df[['gamename', 'date', y]+genres].sort_values(by=y, ascending=order_bool).reset_index()      # Data - Plot 2

# Dataframe preview
title = f"1.1 Dataset of {ax.title().replace('_', ' ')} Games Sorted by :blue[{y_name}]:"
st.subheader(title)
st.dataframe(df_ax)

title = f"1.2 Five {ax.title()} Games with the {order} Monthly :blue[{y_name}]:"
st.subheader(title)
st.write(top_games)



##### PLOT 1 #####
# Plot 1 - markdown
st.markdown(
    """
    ***
    ## 1.0 Individual Game in Category
    Five ranked games from the selected cateogory will be compared from our plot. 
    """
)
# Plot 1 - select box
options = top_games
selected_options = st.multiselect('Select Video Games', options)

# Plot 1
title_names = ','.join(selected_options)
title = f"Monthly :blue[{y_name}] of {title_names} Over Time"
gb = df_ax.sort_values(by='date')
gb_list = {game: gb[gb["gamename"] == game] for game in selected_options}

fig_1 = go.Figure()
fig_1.update_layout(title=title)
for game, gb in gb_list.items():
    fig_1 = fig_1.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=game, mode='lines'))
st.plotly_chart(fig_1)


##### PLOT 2 #####
# Plot 2 - markdown
st.markdown(
    """
    ***
    ## 2.0 Comparison Among Categories
    """
)

# Plot 2 - Multiselect box
options = genres
selected_options = st.multiselect('Select Comparing Categories', options)
selected_names = ','.join(selected_options)                         # formating titles
title = f"Monthly :blue[{y_name}] of {selected_names} Over Time"
st.write(title)



# Plot 2

# Tab 1 - Mean Line Plot
gb = df_bx.sort_values(by='date')      # New copy of df
mean_list = {category: gb[gb[category] == 1].groupby('date').mean(y).reset_index() for category in selected_options}

fig_mean = go.Figure()
for category, gb in mean_list.items():
    fig_mean = fig_mean.add_trace(go.Scatter(x=gb['date'], y=gb[y], name=category, mode='lines'))
fig_mean.update_layout(
    xaxis_title = 'Date',
    yaxis_title = 'Mean of '+y_name,
)


# Tab 2 - Sum Line Plot
gb = df_bx.sort_values(by='date')
sum_list = {category: gb[gb[category] == 1].groupby('date').sum(y).reset_index() for category in selected_options}

fig_sum = go.Figure()
for category, gb in sum_list.items():
    fig_sum = fig_sum.add_trace(go.Scatter(x=gb['date'], y=gb[y], name=category))
fig_sum.update_layout(
    xaxis_title='Date',
    yaxis_title='Sum of '+y_name,
)

# Tab 3 - Scatter / Marker Plot
gb = df_bx.sort_values(by='date')
gb_list = {category: gb[gb[category] == 1] for category in selected_options}

fig_sc = go.Figure()
for category, gb in gb_list.items():
    fig_sc = fig_sc.add_trace(go.Scatter(x=gb["date"], y=gb[y], name=category, mode='markers'))
fig_sc.update_traces(
    marker=dict(size=4, opacity=0.5)
)
fig_sc.update_layout(
    xaxis_title='Date',
    yaxis_title=y_name,
)


# Showing Plot
tab1, tab2, tab3 = st.tabs(['Line Plot', 'Sum Plot', 'Scatter Plot'])
with tab1:
    st.plotly_chart(fig_mean)
with tab2:
    st.plotly_chart(fig_sum)
with tab3:
    st.plotly_chart(fig_sc)

