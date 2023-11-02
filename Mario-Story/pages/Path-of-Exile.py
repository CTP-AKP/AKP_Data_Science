import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
sns.set()
st.title("Path of Exile Visualization")
st.markdown(
    """
    test
    """

)
df = pd.read_csv('../data/SteamCharts.csv',encoding='unicode_escape')

st.write(df.head(2))

select_cond = df['gamename'] == 'Path of Exile'

df_POE = df[select_cond]

st.write(df_POE)

#st.write(df_POE.head(2))
#all poe in my new df. Lets start off with an average for each year.
df_POE['year'] = pd.to_numeric(df_POE['year'])
df_POE.groupby('year').agg('mean')
