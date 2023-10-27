import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
sns.set()


st.header("👋")
st.title("Video Games Plotted")

df = pd.read_csv('..\data/Video_Games.csv')
df.drop_duplicates(inplace=True)
#dataframe now.
st.write("Table containing every col and row of df.")
st.dataframe(df)


#plot bar according to publisher how many games included in df
#select only >25 games. Lots of data, much fluff. Maybe groupby via Publisher needed?

st.write("This bar chart displays how many games have been made by publishers. Helpful to know as some developers are way bigger than others, and therefore may dominate sales.")
select_cond = df['Publisher'].value_counts() > 25
Publisher_Game_Totals =  df['Publisher'].value_counts()[select_cond]
st.bar_chart(Publisher_Game_Totals)

#now mabye percentage of what sales are from NA/JP/OTHER on pie chart
#could show maybe the best markets to target 
#means, compare (region)_sales to global, but this is for each game. maybe
#by publisher

#year of release compared to global sales? since in this dataset, global is 
# num/1million
st.write("Year of release compared to global sales. Showing a trend in the popularity of video games, in the millions. Meaning, 1.0 = 1 Million Copies")
grouping = ['Year_of_Release']
df_YOR = df.groupby(grouping)['Global_Sales'].sum()
df_YOR = pd.DataFrame(df_YOR).reset_index()
st.bar_chart(df_YOR,x="Year_of_Release")