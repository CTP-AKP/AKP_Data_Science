import streamlit as st

from module.__custom__ import *

theme = "Age Restriction"
page_genres = ['age_0_plus', 'age_13_plus', 'age_18_plus']
labels = page_genres

exec_page('👴', theme, page_genres)
plot3_box(theme, labels)