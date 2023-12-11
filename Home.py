import streamlit as st
import random
import time
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from streamlit_extras.stylable_container import stylable_container
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain.vectorstores import Chroma
from streamlit_extras.switch_page_button import switch_page 
from module.__custom__ import *


# load from disk
db = Chroma(
    persist_directory="./data/docs/chroma", 
    embedding_function=embedding
)

emoji = '🕹️ GameInsightify'
st.header(emoji)
st.title("Game Recommender")

# Styling on Tabs
css=f'''
div.stTabs {{
    height: 40vh;
    overflow-y: scroll;
    overflow-x: hidden;
}}
</style>
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'gamenames' not in st.session_state:
    st.session_state.gamenames = []

# Slider on range and button to clear chat history
col1, col2= st.columns([8,2])
with col1: 
    query_num = st.slider(
        label=f'Number of recommendations',
        value = 3, 
        min_value=1, max_value=10, 
    )
with col2: 
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.gamenames = []


# Display chat messages from history on app rerun
tab1, tab2= st.tabs(['Chatbot', ' '])
with tab1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with tab2: 
    pass    # this tab exist becasue i have to limit the height of chatbot


# Accept user input
if prompt := st.chat_input("Need a game recommendation?"):
    st.session_state.messages.append({"role": "user", "content": prompt})       # Add user message to chat history
    with st.chat_message("user"):                                               # Display user message in chat message container
        st.markdown(prompt)


    with st.chat_message("assistant"):                                          # Display assistant response in chat message container
        message_placeholder = st.empty()
        
        docs = db.max_marginal_relevance_search(prompt,k=query_num, fetch_k=10) # Sending query to db
        full_response = random.choice(                                          # 1st sentence of response
            ["I recommend the following games:\n",
            f"Hi, human! The best {query_num} games:\n",
            f"I bet you will love these {query_num} games:\n",]
        )
        
        # formatting response from db
        top_games = []
        assistant_response = ""
        for idx, doc in enumerate(docs):
            gamename = doc.metadata['name']
            top_games.append(gamename)
            assistant_response += f"{idx+1}. {gamename}\n"
        
        # separating response into chunk of words
        chunks = []
        for line in assistant_response.splitlines():
            for word in line.split() : chunks.append(word)
            chunks.append('\n')
        chunks = chunks[0:-1]
        
        # Simulate stream of response with milliseconds delay
        for chunk in chunks:
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")   # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.gamenames.append(top_games)
                
col1, col2, col3= st.columns([4,2,4])
with col2:
    if st.button("Plot Games"):     # button in center column
        switch_page('Overall')

