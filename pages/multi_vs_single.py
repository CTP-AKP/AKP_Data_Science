import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()
import streamlit as st
import altair as alt
# Set the title of the web app
st.title("Multi-player vs Single-player")

# Load the dataset
df = pd.read_csv('./data/SteamCharts.csv', encoding='unicode_escape')
df_st = pd.read_csv('./data/games.csv')
st.markdown(
    """
    How multi-player games behave differently to single-player games
    """
)

# Clean and format the data
df['year'] = df['year'].astype(str).str.strip()
df['month'] = df['month'].astype(str).str.strip()
df['date'] = pd.to_datetime(df['year'] + " " + df['month'], format="%Y %B", errors='coerce')

df_mean = df.groupby(['gamename']).mean(['avg_peak_perc'])
df.columns = df.columns.str.replace(' ', '_')
df_st.columns = df_st.columns.str.replace(' ', '_')
df_st['Release_date'] = pd.to_datetime(df_st['Release_date'])
df_st['Release_year'] = df_st['Release_date'].dt.strftime('%Y')

df.columns = df.columns.str.replace(' ', '_')
df_st.columns = df_st.columns.str.replace(' ', '_')
df_st['Release_date'] = pd.to_datetime(df_st['Release_date'])
df_st['Release_year'] = df_st['Release_date'].dt.strftime('%Y')

df_st = df_st.dropna(subset = ['Name'])
values = {
    "About_the_game": "N/A", 
    "Reviews": "N/A", 
    "Website": "N/A", 
    "Support_url": "N/A", 
    "Support_email": "N/A", 
    "Metacritic_url": "N/A", 
    "Notes": "N/A", 
    "Developers": "N/A", 
    "Publishers": "N/A", 
    "Categories": "Undefined", 
    "Genres": "Undefined", 
    "Tags": "N/A", 
    "Screenshots": "N/A", 
    "Movies": "N/A", 
}
df_st = df_st.fillna(value=values)

values = ['Name', 'DLC_count', 'Release_year']
df_single = df_st[df_st.Categories.str.contains('Single-player')][values]
df_multi = df_st[df_st.Categories.str.contains('Multi-player')][values]
df_dlc = df_st[['Name', 'DLC_count']]

df_single = df_single.rename(columns = {"Name": "gamename"}).set_index('gamename')
df_multi = df_multi.rename(columns = {"Name": "gamename"}).set_index('gamename')
df_dlc = df_dlc.rename(columns = {"Name": "gamename"}).set_index('gamename')


join_multi = df_mean.join(df_multi, how='inner')
join_multi['multi-player'] = 1
join_single = df_mean.join(df_single, how='inner')
join_single['multi-player'] = 0

#dataframe now.
st.write("Single-player games")
st.write(df_single)

st.write("Multi-player games")
st.write(df_multi)

plt.figure(figsize=(10, 6))
sns.lineplot(data=join_single, x='DLC_count', y='peak', label='single-player')
plt.title('Mean of peak score over count of DLC')
plt.xlabel('DLC Count')
plt.ylabel('Mean of Peak score')
st.pyplot(plt)


DLC_year = join_multi.groupby(['Release_year']).sum(['DLC_count'])

plt.figure(figsize=(10, 6))
sns.lineplot(data=DLC_year, x='Release_year', y='DLC_count', label='DLC_count')
plt.title('Mean of peak score over count of DLC')
plt.xlabel('Release year')
plt.ylabel('DLC count')
st.pyplot(plt)