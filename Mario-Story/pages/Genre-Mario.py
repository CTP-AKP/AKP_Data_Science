import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
sns.set()
st.title("Genre")

df = pd.read_csv('..\data/Video_Games.csv')
df.drop_duplicates(inplace=True)
select_cond = df['Name'].str.contains("Mario", na=False)
mario_df = df[select_cond]
st.markdown(
    """
    How has Mario branched out and grown, in a video game sense, from being a basic platformer?
    We know Mario started out as running through levels, trying to get to the top of a flag while avoiding obstacles and saving a princess.
    But Mario has branched out since then to many different genres.
    """
)

# bar chart on mario games by genre
# maybe how many, then how much they each sell etc
select_cond = mario_df['Genre'].value_counts()
mario_genre_totals =  mario_df['Genre'].value_counts()
st.bar_chart(mario_genre_totals)



#dataframe now.
st.write("Splitting up Mario by genre of game. Then, visualize how they perform.")
#so, let me get each mario game row.
st.write(mario_df)
