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
    Attempting to display the player count average of Path of Exile, per year and month.

    Datetime = month(mapped to .01 for each of its place 1-12), + year which is already numeric.
    
    """
)
df = pd.read_csv('../data/SteamCharts.csv',encoding='unicode_escape')

st.write(df.head(2))

select_cond = df['gamename'] == 'Path of Exile'

df_POE = df[select_cond]

st.write(df_POE)

#st.write(df_POE.head(2))
#all poe in my new df. Lets start off with an average of players for each year.
# df_POE['year'] = pd.to_numeric(df_POE['year'])
# POE_year = df_POE.groupby('year')
# st.write(POE_year.head())
# #st.bar_chart(POE_year,y=POE_year['avg'].mean())
# #


month_mapping = {
        'January ': 0.01,
        'February ': 0.02,
        'March ': 0.03,
        'April ': 0.04,
        'May ': 0.05,
        'June ': 0.06,
        'July ': 0.07,
        'August ': 0.08,
        'September ': 0.09,
        'October ': 0.10,
        'November ': 0.11,
        'December ': 0.12
    }
df_POE['datetime'] = df_POE['month'].map(month_mapping)
df_POE['datetime'] = df_POE['datetime'] + df_POE['year']
#so now groupby DATETIME then aggg avg of avg?
df_POE = df_POE.groupby('datetime', as_index=False).agg('mean')
st.write(df_POE)
st.bar_chart(df_POE,x='datetime',y='avg')

st.markdown (
    """

    This would be better visualized by a timeline/line chart. 
    
    """
)

