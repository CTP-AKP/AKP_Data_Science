import streamlit as st

from module.__custom__ import exec_page

theme = "Age Restriction"
page_genres = ['age_0_plus', 'age_13_plus', 'age_18_plus']
exec_page('👴', theme, page_genres)