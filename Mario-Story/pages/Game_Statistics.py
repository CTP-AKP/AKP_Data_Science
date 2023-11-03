import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the web app
st.title("Game Statistics Story")

# Load the dataset
df = pd.read_csv('../data/SteamCharts.csv', encoding='unicode_escape')

# Clean and format the data
df['year'] = df['year'].astype(str).str.strip()
df['month'] = df['month'].astype(str).str.strip()
df['date'] = pd.to_datetime(df['year'] + " " + df['month'], format="%Y %B", errors='coerce')

# 1. "Counter-Strike: Global Offensive" vs "Dota 2"
st.header("Counter-Strike: Global Offensive vs Dota 2")
cs_go = df[df['gamename'] == "Counter-Strike: Global Offensive"]
dota2 = df[df['gamename'] == "Dota 2"]

plt.figure(figsize=(10, 6))
sns.lineplot(data=cs_go, x='date', y='avg', label='CS:GO')
sns.lineplot(data=dota2, x='date', y='avg', label='Dota 2')
plt.title('Average Players Over Time')
plt.xlabel('Date')
plt.ylabel('Average Players')
st.pyplot(plt)

# 2. Comparison of "Path of Exile" vs "The Witcher 3: Wild Hunt"
st.header("Rocket League vs The Witcher 3: Wild Hunt")
path_of_exile = df[df['gamename'] == "Rocket League"]
the_witcher_3 = df[df['gamename'] == "The Witcher 3: Wild Hunt"]

plt.figure(figsize=(10, 6))
sns.lineplot(data=path_of_exile, x='date', y='avg', label='Path of Exile')
sns.lineplot(data=the_witcher_3, x='date', y='avg', label='The Witcher 3: Wild Hunt')
plt.title('Average Players Over Time: Single vs Multiplayer')
plt.xlabel('Date')
plt.ylabel('Average Players')
st.pyplot(plt)

# 3. Most popular game in the Assassin's Creed series
st.header("Popularity of Assassin's Creed Games")
assassins_creed_games = df[df['gamename'].str.contains("Assassin's Creed")]

# Group by game name and sum up average players
ac_popularity = assassins_creed_games.groupby('gamename')['avg'].sum().reset_index()

# Bar plot of average players for each Assassin's Creed game
plt.figure(figsize=(10, 6))
sns.barplot(data=ac_popularity, x='avg', y='gamename')
plt.title('Popularity of Assassin’s Creed Games')
plt.xlabel('Total Average Players')
plt.ylabel('Game')
st.pyplot(plt)

# 4. Player count changes during world events (hypothetical)
st.header("Player Count Changes During Covid-19 in Dota 2")
dota2_covid = dota2[(dota2['date'] >= '2019-01-01') & (dota2['date'] <= '2020-12-31')]

plt.figure(figsize=(10, 6))
sns.lineplot(data=dota2_covid, x='date', y='avg')
plt.axvline(x=pd.to_datetime('2020-03-11'), color='red', linestyle='--', label='Covid-19 Declared')
plt.title('Dota 2 Player Count During Covid-19')
plt.xlabel('Date')
plt.ylabel('Average Players')
plt.legend()
st.pyplot(plt)

# 5. Games with the highest peak of players (Pie Chart)
st.header("Games with the Highest Peak of Players")

# Group by game name and get the max peak players
peak_players = df.groupby('gamename')['peak'].max().sort_values(ascending=False).head(5)

# Pie chart of peak players for top games
fig, ax = plt.subplots()
ax.pie(peak_players, labels=peak_players.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Top 5 Games with Highest Peak of Players')
st.pyplot(fig)





