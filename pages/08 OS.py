import streamlit as st

from module.__custom__ import *

theme = "OS"
page_genres = ['windows', 'mac', 'linux', 'not_windows', 'not_mac', 'not_linux']
add_genres = [['not_windows', 'windows'], ['not_mac', 'mac'], ['not_linux', 'linux'] ]
labels = ['not_windows', 'windows']
labels_2 = ['not_mac', 'mac']
labels_3 = ['not_linux', 'linux']

# ### adding single-player feature ###
for add in add_genres:
       add_opp_features(add)
exec_page('🖥', theme, page_genres)
tab1, tab2, tab3 = st.tabs(['Windows game ratio', 'Mac game ratio', 'Linux game ratio'])
with tab1:
       plot3_box(theme, labels)
with tab2:
       plot3_box(theme, labels_2)
with tab3:
       plot3_box(theme, labels_3)