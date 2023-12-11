import streamlit as st
from streamlit_extras.switch_page_button import switchpage 
import os

pages = ["Overall"]

files = os.listdir('.\pages')  # Assuming your files are in the 'pages' directory
for name in files:
    if name.endswith('.py'):  # Check if the file is a Python file
        name = name.split('', 1)[1]  # Split on the first underscore and take the second part
        name = name.replace('.py', '').replace('_', ' ')  # Replace underscores with spaces and remove '.py'
        pages.append(name)

def st_page_selectbox(current_page):
    current_index = pages.index(current_page)
    selected_page = st.selectbox("Select a category", pages, index=current_index)
    if selected_page != current_page:
        switch_page(selected_page)