import streamlit as st
import pandas as pd
from recommender import CosineGameRecommended

def show_recommender_interface():
    st.markdown("""
        Using content-based filtering, we created a Video Game Recommender for the average gamer, based on Steam.
    """)

    dataframe = pd.read_csv('data/cosine.csv')

    slider_count = st.slider(label="How many recommended games do you want?", min_value=5, max_value=50)
    options = st.selectbox(label="What game would you like recommendations from?", options=dataframe['Name'])

    if st.button(label="Give me recommendations!"):
        recommended_df = CosineGameRecommended(options, slider_count)
        if recommended_df is not None:
            st.write(recommended_df)
