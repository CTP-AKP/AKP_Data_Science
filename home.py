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
st.title("When Will Your Favorite Game Die?")
# st.title("Video Game Lifespan in Relation to Other Features")

# Markdown
st.markdown(
    """
    This project visualizes how different factors affect the lifespan of a video game. This is our dataset. Player counts of video games are recorded on a monthly basis. 
    """
)


# Dataframe Preview
# st.write("This is our dataset. Player counts of video games are recorded on a monthly basis. ")
st.dataframe(df)

# Plot 1
st.subheader('1.0 Player Gained by Month :blue[(Gain)] :sunglasses:')
st.write(
    "These are the 5 games with the lowest gain within a month. They are negative which indicates this game lost players in total. "
)

# Plot 1 - selected dataframe preview
df_sort_gain = df.sort_values(by=['gain'])[['gamename', 'gain']].reset_index()
st.dataframe(df_sort_gain.head())


cyberpunk2077 = df['gamename']=='Cyberpunk 2077'
fallout4 = df['gamename']=='Fallout 4'
grand_theft_auto_v = df['gamename']=='Grand Theft Auto V'
monster_hunter_world = df['gamename']=='Monster Hunter: World'
csgo = df['gamename']=='Counter-Strike: Global Offensive'
dota2 = df['gamename']=='Dota 2'
destiny2 = df['gamename']=='Destiny 2'
team_fortress2 = df['gamename']=='Team Fortress 2'

gb = df[fallout4 | grand_theft_auto_v | monster_hunter_world | cyberpunk2077 | dota2]
gb = gb.reset_index()
st.line_chart(gb, x="date", y="avg", color="gamename")
st.line_chart(gb, x="date", y="gain", color="gamename")

gb = df[fallout4 | destiny2 | grand_theft_auto_v ]
gb = gb.reset_index()
st.line_chart(gb, x="date", y="peak", color="gamename")
st.line_chart(gb, x="date", y="avg", color="gamename")


st.write("Multi-player vs Single-player.")
gb = df.groupby(['date', 'multi_player']).mean('avg')
gb = gb.reset_index()
st.line_chart(df, x="date", y="avg", color="multi_player")
st.line_chart(gb, x="date", y="avg", color="multi_player")

# fallout4 = df[df['gamename']=='Fallout 4']
# grand_theft_auto_v = df[df['gamename']=='Grand Theft Auto V']
# monster_hunter_world = df[df['gamename']=='Monster Hunter: World']
# ax = plt.figure(figsize=(10, 6))
# ax = sns.lineplot(x="date", y="avg", data=fallout4, label='Fallout 4') 
# ax = sns.lineplot(x="date", y="avg", data=grand_theft_auto_v, label='grand_theft_auto_v') 
# ax = sns.lineplot(x="date", y="avg", data=monster_hunter_world, label='monster_hunter_world') 
# st.pyplot(plt)
