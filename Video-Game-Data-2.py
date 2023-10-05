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
df.drop_duplicates(inplace=True)
#dataframe now.
st.write("Table containing every col and row of df.")
st.dataframe(df)
#plot bar according to publisher how many games included in df
value_counts = df['Publisher'].value_counts()
#removing according to value_counts < whatever number. Tons of data, much is
#fluff
# to_remove = value_counts[value_counts <= 25].index
# df = df[~df.Publisher.isin(to_remove)]
select_cond = df['Publisher'].value_counts() > 25
Publisher_Game_Totals =  df['Publisher'].value_counts()[select_cond]
st.bar_chart(Publisher_Game_Totals)
#used matplotlib but dont rlly like it