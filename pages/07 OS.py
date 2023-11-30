import streamlit as st

from module.__custom__ import *

theme = "OS"
page_genres = ['windows', 'mac', 'linux', 'not_windows', 'not_mac', 'not_linux']
add_genres = [['not_windows', 'windows'], ['not_mac', 'mac'], ['not_linux', 'linux'] ]

# ### adding single-player feature ###
for add in add_genres:
       add_opp_features(add)
exec_page('🖥', theme, page_genres)