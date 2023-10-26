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
st.bar_chart(df,x="Name",y=y_cond)

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
    In this next scatter plot, the FARTHER they are from the Y axis, the more average playtime
    """
)

alt_chart = alt.Chart(df_CCU).mark_circle(size=60).encode(
    x='Median playtime forever',
    y='Average playtime forever',
    tooltip = ['Name']
).interactive()
st.altair_chart(alt_chart)



