# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

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
    How multi-player games behave differently to single-player games
    """
)


#dataframe now.
st.write("Table containing every col and row of df.")
st.dataframe(df)


st.write("This bar chart displays how many games have been made by publishers. Helpful to know as some developers are way bigger than others, and therefore may dominate sales.")
# select_cond = df['publishers'].value_counts() > 25
# Publisher_Game_Totals =  df['publishers'].value_counts()[select_cond]
# st.bar_chart(Publisher_Game_Totals)


df_sort_gain = df.sort_values(by=['gain'])[['gamename', 'gain']]
st.dataframe(df_sort_gain)


cyberpunk2077 = df['gamename']=='Cyberpunk 2077'
fallout4 = df['gamename']=='Fallout 4'
grand_theft_auto_v = df['gamename']=='Grand Theft Auto V'
monster_hunter_world = df['gamename']=='Monster Hunter: World'

gb = df[fallout4 | grand_theft_auto_v | monster_hunter_world | cyberpunk2077]
gb = gb.reset_index()
st.line_chart(gb, x="date", y="avg", color="gamename")
st.line_chart(gb, x="date", y="gain", color="gamename")


# fallout4 = df[df['gamename']=='Fallout 4']
# grand_theft_auto_v = df[df['gamename']=='Grand Theft Auto V']
# monster_hunter_world = df[df['gamename']=='Monster Hunter: World']
# ax = plt.figure(figsize=(10, 6))
# ax = sns.lineplot(x="date", y="avg", data=fallout4, label='Fallout 4') 
# ax = sns.lineplot(x="date", y="avg", data=grand_theft_auto_v, label='grand_theft_auto_v') 
# ax = sns.lineplot(x="date", y="avg", data=monster_hunter_world, label='monster_hunter_world') 
# st.pyplot(plt)
