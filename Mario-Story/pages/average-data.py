import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import matplotlib.ticker as ticker
sns.set()

df = pd.read_csv('../data/join_02.csv',encoding='unicode_escape')

df.date = pd.to_datetime(df.date)
df.release_date = pd.to_datetime(df.release_date)
st.title('Averaging Games through Lifespan')

st.markdown(
    """
    A good place to get started would be defining what the lifespan of a game is. Now this varies from the type of game, but overall it's the timeline of players
    and longevity of said players. How long people are playing your game for, no matter the reason.
    """

)

st.write(df.head())

st.markdown(
    """
    Lets start by grouping multiplayer, singleplayer.
    """

)

select_cond = df['multi_player'] == 1 #multiplayer game selector
df_MP = df[select_cond]

st.markdown(
    """
    Multiplayer Dataframe
    """
)
st.write(df_MP)

select_cond = df['multi_player'] == 0 #singleplayer game selector
df_SP = df[select_cond]

st.markdown(
    """
    Singleplayer Dataframe
    """
)
st.write(df_SP)

st.markdown(
    """
    Now lets start to picture the best singleplayer and multiplayer games.
    """
)



MP_max_peak = df_MP['peak'].max()
select_cond = df_MP['peak'] == 1305714
df_MP_max = df_MP[select_cond]
st.write(df_MP_max)


SP_max_peak = df_SP['peak'].max()
select_cond = df_SP['peak'] == 830387
df_SP_max = df_SP[select_cond]
st.write(df_SP_max)


select_cond = (df_SP['avg'] > 20000)
df_SP = df_SP[select_cond]

#so maybe, display avg for each game, per month. then we can average the avg out since these are all singleplayer games.
#but may have to group by release date anyway. or show it through analysis

average_singleplayer = df_SP['avg'].mean()
median_singleplayer = df_SP['avg'].median()
average_multiplayer = df_MP['avg'].mean()
median_multiplayer = df_MP['avg'].median()

#so, lets median from all games, grouped by date


df_SP = df_SP.groupby('date', as_index=False)['avg'].agg('mean')
st.write(df_SP)
fig = plt.figure(figsize=(10,4))
sns.lineplot(x='date', y='avg',data=df_SP)
st.pyplot(fig)






st.markdown(
    """
    For reference purposes:  
    avg: average players in the given year + month  
    gain: difference in average players compared to previous month  
    avg_peak_perc: avg / peak. How far away are we from our peak players  
    dlc_count: Downloadable content released. May or may not be free.  
    metacritic_score: rating from site metacritic  
    positive: # of positive reviews  
    negative: # of negative reviews  
    developers: the actual creators of the game  
    publisher: takes the product and finds ways to make money  
    average_playtime_forever: avg playtime all time for every owner   
    average_playtime_two_weeks: average playtime over 2 weeks   
    median_playtime_forever: the median playtime forever  
    median_playtime_two_weeks: median two weeks time  
    """
)
