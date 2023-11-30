import streamlit as st

from module.__custom__ import *

theme = "Settings"
page_genres = ['full_audio', 'full_controller_support', 'not_full_audio', 'not_full_controller']
add_genres = [['not_full_audio', 'full_audio'], ['not_full_controller', 'full_controller_support'] ]

# ### adding single-player feature ###
for add in add_genres:
       add_opp_features(add)
exec_page('🎧', theme, page_genres)