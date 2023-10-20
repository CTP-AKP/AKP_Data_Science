import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.header("👋")
st.title("Sold by Year")

df = pd.read_csv('..\data/Video_Games.csv')
df.drop_duplicates(inplace=True)
select_cond = df['Name'].str.contains("Mario", na=False)
mario_df = df[select_cond]

st.markdown(
    """
        Correlation does not equal causation. But, it would be safe to assume if there is more sales of a game, that means theres more money.
        Then, maybe Nintendo would be willing to experiment more with what types of games they make. Including Mario
    """
)

#so now I want to put total sales, and see how they scale according to years. Then, we can correlate the years to when the other genre games were released.
#group by year?

mario_YOR_df = df.groupby('Year_of_Release')
YOR_graph = mario_YOR_df['Global_Sales'].count()

st.bar_chart(YOR_graph)
