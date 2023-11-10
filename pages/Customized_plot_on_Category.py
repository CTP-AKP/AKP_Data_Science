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
# ### adding single-player feature ###
df['single_player'] = (df['multi_player']==0)*1

# Header
st.header("👋")
st.title("Customized Plot on :blue[Category]")

##### FILTER #####
# Featuer for both axis
features = ['avg', 'gain', 'peak', 'avg_peak_perc']
features += ['metacritic_score', 'positive', 'negative']
genres = ['multi_player', 'pvp', 'co-op', 'single_player']

left_col, right_col = st.columns(2)
order = st.toggle(label='Find the Worst Games', value=False)   # descending order toggle switch
with left_col: y = st.selectbox("Select a Feature", features)       # feature select box
with right_col: ax = st.selectbox("Select a Category", genres)     # category select box
order_name='Worst' if order else 'Highest'                          # string formating
y_name = y.replace('_', ' ').title()
ax_name = ax.title().replace('_', ' ')

# Data - sorting and filtering
df_ax = df[df[ax]==1]
df_ax = df_ax[['gamename', 'date', y, ax]].sort_values(by=y, ascending=order).reset_index()    # Data - Plot 1
top_games = df_ax.gamename.unique()[0:5]
df_bx = df[['gamename', 'date', y]+genres].sort_values(by=y, ascending=order).reset_index()      # Data - Plot 2

# Dataframe preview
title = f"1.1 Dataset of :blue[{ax_name}] Games Sorted by :blue[{y_name}]:"
st.subheader(title)
st.dataframe(df_ax)

title = f"1.2 Five :blue[{ax_name}] Games with the :red[{order_name}] Monthly :blue[{y_name}]:"
st.subheader(title)
st.write(top_games)



##### PLOT 1 #####
# Plot 1 - markdown
st.markdown("""***""")
title = f"1.3 :blue[{ax_name}] Games with the :red[{order_name}] :blue[{y_name}]"
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


##### PLOT 2 #####
# Plot 2 - markdown
st.markdown("""***""")
title = f"2.0 Comparison Among :blue[Game Categories] on Monthly :blue[{y_name}]:"
st.subheader(title)

# Plot 2 - Multiselect box
options = genres
selected_options = st.multiselect('Select Comparing Categories', options)
selected_names = ','.join(selected_options)                         # formating titles
plot_title = f"Monthly {y_name} of {selected_names} Over Time"



# Plot 2

# Tab 1 - Mean Line Plot
gb = df_bx.sort_values(by='date')      # New copy of df
mean_list = {category: gb[gb[category] == 1].groupby('date').mean(y).reset_index() for category in selected_options}

fig_mean = go.Figure()
for category, gb in mean_list.items():
    fig_mean = fig_mean.add_trace(go.Scatter(x=gb['date'], y=gb[y], name=category, mode='lines'))
fig_mean.update_layout(
    title = 'Mean of '+ plot_title, 
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
    title = 'Sum of '+ plot_title, 
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
    title = plot_title, 
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

