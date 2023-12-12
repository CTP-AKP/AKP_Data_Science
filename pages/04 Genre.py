import streamlit as st

from module.__custom__ import *

theme = "Genre"
page_genres = ['genre_action', 'genre_adventure', 'genre_casual',
       'genre_sexual_content', 'genre_strategy', 'genre_sports',
       'genre_racing', 'genre_rpg', 'genre_simulation', 'indie', 'mainstream']
add_genre = ['mainstream', 'indie']
labels = ['genre_action', 'genre_adventure', 'genre_casual',
       'genre_sexual_content', 'genre_strategy', 'genre_sports',
       'genre_racing', 'genre_rpg', 'genre_simulation']
labels_2 = add_genre

add_opp_features(add_genre)
exec_page('🦹‍♀️', theme, page_genres)

tab1, tab2= st.tabs(['Genre ratio', 'Indie versus mainstream ratio'])
with tab1:
       plot3_box(theme, labels)
with tab2:
       plot3_box(theme, labels_2)