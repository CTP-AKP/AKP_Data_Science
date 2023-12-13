import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
import os

pages = ["Home"]

files = os.listdir('.\pages')
for name in files:
    name = name.split()[1].replace('.py', '').replace('_', ' ')
    pages.append(name)


def st_page_selectbox(current_page):
    current_index = pages.index(current_page)
    selected_page = st.selectbox("Select a category", pages, index=current_index)
    if selected_page != current_page:
        switch_page(selected_page)
