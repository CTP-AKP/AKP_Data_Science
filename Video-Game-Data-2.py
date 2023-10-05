import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
sns.set()


st.header("👋")
st.title("Video Games Plotted")

df = pd.read_csv('data/Video_Games.csv')
df.drop_duplicates()
#dataframe now.
st.write("Table containing every col and row of df.")
st.dataframe(df)
#plot bar according to publisher how many games included in df
value_counts = df['Publisher'].value_counts()
#removing according to value_counts < whatever number. Tons of data, much is
#fluff
to_remove = value_counts[value_counts <= 25].index
df = df[~df.Publisher.isin(to_remove)]
publisher_sum = df['Publisher'].value_counts()
#st.bar_chart(publisher_sum)
c = (alt.Chart(publisher_sum).mark_bar().encode(
    x='value_counts():Q',
    y="Publisher:O") )
st.altair_chart(c, use_container_width=True)
#used matplotlib but dont rlly like it