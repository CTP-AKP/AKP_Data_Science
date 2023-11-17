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
from module.__custom30__ import *
sns.set()

# Load the dataset
df = pd.read_csv('./data/join_02.csv')

# Format preparation
df['date'] = pd.to_datetime(df['date'])
df['release_date'] = pd.to_datetime(df['release_date'])
df['avg_peak_perc'] = df['avg_peak_perc'].str.rstrip('%').astype('float') 
df = df.dropna()
# ### will add best publisher features below ###


# Header
st.header("🛒 ForcaSteam")
st.title("Recommending a Game Based on Your :blue[Habits]")

##### FILTER #####
# year_first = datetime.date(2020, 1, 1)
# year_last = datetime.date(2023, 1, 1)
# now = datetime.datetime.now(),
years = np.arange(1990, 2023)
ages = ['age_0_plus', 'age_13_plus', 'age_18_plus']
prices = ['price_free', 'price_5', 'price_15', 'price_20', 'price_40', 'price_60', 'price_most']
dlcs = ['dlc_0', 'dlc_5', 'dlc_15', 'dlc_40', 'dlc_100', 'dlc_300', 'dlc_most']
oss = ['windows', 'mac', 'linux']
categories = ['pvp', 'co-op', 'single_player']
genres = ['genre_action', 'genre_adventure', 'genre_casual',
       'genre_sexual_content', 'genre_strategy', 'genre_sports',
       'genre_racing', 'genre_rpg', 'genre_simulation', 'indie', 'mainstream']
settings = ['full_audio', 'full_controller_support']

add_opp = [['single_player', 'multi_player'], ['mainstream', 'indie']]
add_range = [[0, 0.001, 'price_free', 'price'], 
              [0.001, 5.001, 'price_5', 'price'],
              [5.001, 10.001, 'price_10', 'price'],
              [10.001, 15.001, 'price_15', 'price'],
              [15.001, 20.001, 'price_20', 'price'],
              [20.001, 40.001, 'price_40', 'price'],
              [40.001, 60.001, 'price_60', 'price'], 
              [60.001, 9999, 'price_most', 'price'], 
              [0, 1, 'dlc_0', 'dlc_count'], 
              [1, 6, 'dlc_5', 'dlc_count'],
              [6, 16, 'dlc_15', 'dlc_count'],
              [16, 41, 'dlc_40', 'dlc_count'],
              [41, 101, 'dlc_100', 'dlc_count'],
              [101, 301, 'dlc_300', 'dlc_count'],
              [301, 9999, 'dlc_most', 'dlc_count']]


for add in add_opp:
       add_opp_features(add)
for add in add_range:
       add_range_features(add)

left_col, right_col = st.columns(2)
with left_col:
    release_year = st.selectbox("Select a release year", years)
    prices = st.selectbox("Select a price range", prices)
    os = st.multiselect('Select your OS', oss)
    category = st.multiselect('Select preferred categoris', categories)
    setting = st.multiselect('Select preferred settings', settings)
    
    
with right_col:
    age = st.selectbox("Select a age restriction", ages)
    dlc_count = st.selectbox("Select a dlc range", dlcs)
    avg_playtime = st.slider(
        label=f'Select range of playtime in 2 weeks',
        value = (1, 5),
        min_value=1, max_value=1000, 
    )
    genre = st.multiselect('Select preferred genres', genres)
    

# ### adding best publisher features feature ###
