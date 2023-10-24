import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.header("👋")
st.title("Sold by Year")

df = pd.read_csv('..\data/games.csv')

st.write(df.head())

st.markdown(
    """
    This dataset is a bunch of stats about steam games, including concurrent players from the day the data was updated (3 months ago).
    """

)