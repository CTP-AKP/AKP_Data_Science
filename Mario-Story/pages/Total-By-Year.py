import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


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
grouping = ['Year_of_Release']
mario_YOR_DF = df.groupby(grouping)['Global_Sales'].sum()

st.bar_chart(mario_YOR_DF)


st.markdown(
    """
        So we know there is a similar increase in sales, maybe to do with game releases.
        Let's see how the sales by genre perform. Keeping in mind the release count.
    """
)
grouping = ['Genre']
#so group where genre is the same. then sum up global sales for each genre.

mario_df_GYOR = df.groupby(grouping)['Global_Sales'].sum()
mario_df_GYOR = pd.DataFrame(mario_df_GYOR).reset_index()

labels = list(mario_df_GYOR['Genre'].unique())
fig, ax = plt.subplots()
ax.pie(mario_df_GYOR['Global_Sales'],labels=labels,autopct='%1.1f%%',radius=1.3)
st.pyplot(fig)
st.markdown(
    """ 
        Suprisingly, Mario despite starting off as a basic 2d platformer, actually gets a lot more sales from 'Action' and 'Sports'.
        \n- Aside: On this dataset, some 'golf' games are considered 'action'. I dont think golf is that action-packed, but maybe question the reliability of other stats.
        \n- Another aside: 'action' apparently has only 4 games despite being the biggest in sales? Either they are really popular or..
    """
)

#pie chart might make more sense

st.bar_chart(mario_df_GYOR,x='Genre')
