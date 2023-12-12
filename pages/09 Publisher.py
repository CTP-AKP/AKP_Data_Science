import streamlit as st

from module.__custom__ import *

theme = "Publisher"
main_genre = "publishers"
labels = main_genre

exec_page_pub('🛒', theme, main_genre)
plot3_box_limit(theme, labels, 0.01)