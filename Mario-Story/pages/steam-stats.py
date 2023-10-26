import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.header("👋")
st.title("Concurrency")

df = pd.read_pickle('../data/pk-games.pk1')



st.markdown(
    """
    This dataset is a bunch of stats about steam games, including concurrent players from the day the data was updated (3 months ago).
    """
)

columns = list(df.select_dtypes(include='number'))
y_cond = st.selectbox('Pick column to display', columns)
#st.bar_chart(df,x="Name",y=y_cond)

st.markdown(
    """
    Data is a bit too big to see. Must specify more.
    Check Max CCU(Max Concurrent Players) for more than 15000 and then see Average Playtime 2week vs forever. Should show us if the game is STILL lasting or not.
    Why 15000? Modern games typically sit above 15k, and this stat is only for filtering out false positives. Games that have fallen off since.
    """
)

select_cond = df['Peak CCU'] > 15000
df_CCU = df[select_cond]
st.bar_chart(df_CCU,x='Name',y='Peak CCU')
st.write(df_CCU.shape)
st.markdown(
    """
    So, there are 112 games above 15k, so lets further refine our search.
    Now we can try to see games the game's average playtime over two weeks, in minutes, to see if the games are still "alive"
    """
)
#Check for the most 2 week average/median playtime, and then see release date for anomalies
scat_PT = alt.Chart(df_CCU).mark_circle(size=60).encode(
    x='Average playtime two weeks',
    y='Median playtime two weeks',
    color='Average playtime two weeks',
    tooltip =['Name','Release date','Average playtime two weeks','Median playtime two weeks'],
).properties(
        width = 1000,
        height = 500 
    )

#want to ask, median exposes if we have outliers? Someone playing 10x the average, will skew the average, but the median will just get the middle of all data.

st.altair_chart(scat_PT)
select_cond = df_CCU['Average playtime two weeks'] > 500
df_outliers=df_CCU[select_cond]
select_cond =  df_CCU['Median playtime two weeks'] > 500
df_outliers = df_outliers[select_cond]
st.write(df_outliers)
st.write(df_outliers.shape)

st.markdown(
    """
    So there are 36 games that fit our outliers. 
    Slowly through filtering, we see games that were MASSIVE "Hogwarts Legacy with Peak CCU of 872000 people", aren't even holding above 8 hours of playtime in two weeks
    """

)
