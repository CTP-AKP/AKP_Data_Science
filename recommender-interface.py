import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
import pickle
from streamlit import session_state as session
from recommender import CosineGameRecommended
import altair as alt
st.cache(persist=True, show_spinner=False, suppress_st_warning=True)

recommended_df = None
dataframe = pd.read_csv('data\cosine.csv')
st.markdown (
    """
    Using content-based filtering, we created a Video Game Recommender for the average gamer, based on Steam.
    """
)

session.slider_count = st.slider(label="How many recommended games do you want?", min_value=5, max_value=50)

st.text("")
st.text("")

session.options = st.selectbox(label="What game would you like recommendations from?", options=dataframe['Name'])

st.text("")
st.text("")

buffer1, col1, buffer2 = st.columns([1.45, 1, 1])

is_clicked = col1.button(label="Give me recommendations!")

if is_clicked:
    recommended_df = CosineGameRecommended(session.options,session.slider_count)


st.text("")
st.text("")
st.text("")
st.text("")

if dataframe is not None:
    st.write(recommended_df)








