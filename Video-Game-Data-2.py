import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
sns.set()

# Setting up the sidebar for navigation
st.sidebar.header('Navigation')
selection = st.sidebar.radio('Go to', ['Home', 'AG_Mario Kart Analysis'])

if selection == 'Home':
    st.header("👋")
    st.title("Video Games Plotted")

    df = pd.read_csv('data/Video_Games.csv')
    df.drop_duplicates(inplace=True)

    # dataframe now.
    st.write("Table containing every col and row of df.")
    st.dataframe(df)

    # plot bar according to publisher how many games included in df
    # select only >25 games. Lots of data, much fluff. Maybe groupby via Publisher needed?
    st.write("This bar chart displays how many games have been made by publishers. Helpful to know as some developers are way bigger than others, and therefore may dominate sales.")
    select_cond = df['Publisher'].value_counts() > 25
    Publisher_Game_Totals =  df['Publisher'].value_counts()[select_cond]
    st.bar_chart(Publisher_Game_Totals)

    #now mabye percentage of what sales are from NA/JP/OTHER on pie chart
    #could show maybe the best markets to target 
    #means, compare (region)_sales to global, but this is for each game. maybe
    #by publisher

    # year of release compared to global sales? since in this dataset, global is 
    # num/1million
    st.write("Year of release compared to global sales. Showing a trend in the popularity of video games, in the millions. Meaning, 1.0 = 1 Million Copies")
    grouping = ['Year_of_Release']
    df_YOR = df.groupby(grouping)['Global_Sales'].sum()
    df_YOR = pd.DataFrame(df_YOR).reset_index()
    st.bar_chart(df_YOR, x="Year_of_Release")

elif selection == 'AG_Mario Kart Analysis':
    # Narrative Introduction
    st.header("AG_ The Evolution of Mario Kart")
    st.write("""
    **Mario Kart** is a staple in the world of video games. As one of Nintendo's most iconic series, it has captured the hearts of millions worldwide.
    But how has it fared in terms of sales over the years? How do critics and users view it? Let's dive in.
    """)

    df = pd.read_csv('data/Video_Games.csv')  # Reading the data again for this analysis
    mario_kart_df = df[df['Name'].str.contains("Mario Kart", na=False)]

    # Enhanced Sales Visualization
    sales_chart = alt.Chart(mario_kart_df).mark_bar().encode(
        x='Year_of_Release:O',
        y='Global_Sales',
        color=alt.Color('Global_Sales', scale=alt.Scale(scheme='viridis')),
        tooltip=['Name', 'Global_Sales', 'Year_of_Release']
    ).properties(
        width=600,
        height=400,
        title='Mario Kart Global Sales Over Time'
    )
    st.altair_chart(sales_chart, use_container_width=True)

    st.write("""
    The sales trend clearly showcases the consistent appeal of Mario Kart games. With each new release, the game brings substantial sales, affirming its position as a beloved franchise.
    """)

    # Enhanced Score Visualization
    scores_chart = alt.Chart(mario_kart_df).mark_line(point=True).encode(
        x='Year_of_Release:O',
        y='User_Score',
        color=alt.value('green'),
        tooltip=['Name', 'User_Score', 'Year_of_Release']
    ).properties(
        width=600,
        height=400,
        title='User Scores of Mario Kart Games Over Time'
    ) + alt.Chart(mario_kart_df).mark_line(point=True).encode(
        x='Year_of_Release:O',
        y='Critic_Score',
        color=alt.value('red'),
        tooltip=['Name', 'Critic_Score', 'Year_of_Release']
    )

    st.altair_chart(scores_chart, use_container_width=True)

    st.write("""
    The dual line graph paints a compelling picture about the game's reception. While users and critics may not always agree, it's evident that both groups have maintained a favorable view of the Mario Kart series over the years.
    """)