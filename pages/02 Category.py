import streamlit as st

from module.__custom__ import *

theme = "Category"
page_genres = ['multi_player', 'pvp', 'co-op', 'single_player']
add_genre = ['single_player', 'multi_player']
labels = ['pvp', 'co-op', 'single_player']

add_opp_features(add_genre)
exec_page('🤼', theme, page_genres)
plot3_box(theme, labels)