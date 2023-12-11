import streamlit as st

from module.__custom__ import *

theme = "Price"
page_genres = ['price_free', 'price_5', 'price_15', 'price_20', 'price_40', 'price_60', 'price_most']
add_genres = [[0, 0.001, 'price_free', 'price'], 
              [0.001, 5.001, 'price_5', 'price'],
              [5.001, 10.001, 'price_10', 'price'],
              [10.001, 15.001, 'price_15', 'price'],
              [15.001, 20.001, 'price_20', 'price'],
              [20.001, 40.001, 'price_40', 'price'],
              [40.001, 60.001, 'price_60', 'price'], 
              [60.001, 9999, 'price_most', 'price']]

# ### adding single-player feature ###
for add in add_genres:
       add_range_features(add)
exec_page('💸', theme, page_genres)