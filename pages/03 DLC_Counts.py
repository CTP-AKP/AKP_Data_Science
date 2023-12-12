import streamlit as st

from module.__custom__ import *

theme = "DLC Counts"
page_genres = ['dlc_0', 'dlc_5', 'dlc_15', 'dlc_40', 'dlc_100', 'dlc_300', 'dlc_most']
add_genres = [[0, 1, 'dlc_0', 'dlc_count'], 
              [1, 6, 'dlc_5', 'dlc_count'],
              [6, 16, 'dlc_15', 'dlc_count'],
              [16, 41, 'dlc_40', 'dlc_count'],
              [41, 101, 'dlc_100', 'dlc_count'],
              [101, 301, 'dlc_300', 'dlc_count'],
              [301, 9999, 'dlc_most', 'dlc_count']]
labels = 'dlc_count'


# ### adding single-player feature ###
for add in add_genres:
       add_range_features(add)
exec_page('🪜', theme, page_genres)
plot3_box(theme, labels)