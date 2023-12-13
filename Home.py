import streamlit as st
import os
import random
import time
from module.__custom__ import *
from streamlit_extras.switch_page_button import switch_page

# Openai API Key
import openai 
import json
def read_api_key_from_secrets(file_path='secrets.json'):
    try:
        with open(file_path, 'r') as secrets_file:
            secrets_data = json.load(secrets_file)
            openai_api_key = secrets_data.get('openai_api_key')
            
            if openai_api_key is not None:
                return openai_api_key
            else:
                raise KeyError("'openai_api_key' not found in secrets.json")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON in {file_path}. Please check the file format.")

# Example usage
try:
    key = read_api_key_from_secrets()
    openai.api_key = key
    os.environ['OPENAI_API_KEY'] = key
    print(f"OpenAI API Key Found")
except (FileNotFoundError, ValueError, KeyError) as e:
    print(f"Error: {e}")

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
embedding = OpenAIEmbeddings()
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# LLM
from langchain.chat_models import ChatOpenAI
llm_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=llm_name, temperature=0)

# load from disk
db_cos = Chroma(
    persist_directory="./data/docs/chroma_cos", 
    embedding_function=embedding
)
db_plot = Chroma(
    persist_directory="./data/docs/chroma_plot", 
    embedding_function=embedding
)

metadata_field_info = [
    AttributeInfo(
        name="name",
        description="The name of the video game on steam",
        type="string",
    )
]
document_content_description = "Brief summary of a video game on Steam"


with st.sidebar: is_plot = st.toggle('Enable Plot')
db_selected = db_cos
if is_plot: db_selected = db_plot


retriever = SelfQueryRetriever.from_llm(
    llm,
    db_selected,
    document_content_description,
    metadata_field_info,
    enable_limit=True, 
)

emoji = '🕹️ GameInsightify'
st.header(emoji)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'gamenames' not in st.session_state:
    st.session_state.gamenames = []

# Slider on range and button to clear chat history
col1, col2= st.columns([8,2])
with col1: 
    st.title("Game Recommender")
with col2: 
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.gamenames = []


# Display chat messages from history on app rerun
tab1, tab2= st.tabs(['Chatbot', ' '])
with tab1:          # this tab exist becasue i have to limit the height of chatbot
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with tab2: pass    # this tab exist becasue i have to limit the height of chatbot


# Accept user input
if prompt := st.chat_input("Need a game recommendation?"):
    st.session_state.messages.append({"role": "user", "content": prompt})       # Add user message to chat history
    with st.chat_message("user"):                                               # Display user message in chat message container
        st.markdown(prompt)


    with st.chat_message("assistant"):                                          # Display assistant response in chat message container
        message_placeholder = st.empty()
        
        # docs = db.max_marginal_relevance_search(prompt,k=query_num, fetch_k=10) # Sending query to db
        docs = retriever.invoke(prompt)                                         # retrieve response from chatgpt
        full_response = random.choice(                                          # 1st sentence of response
            ["I recommend the following games:\n",
            f"Hi, human! These are the {len(docs)} best games:\n",
            f"I bet you will love these {len(docs)} games:\n",]
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
    if is_plot: st.session_state.gamenames.append(top_games)
                
col1, col2, col3= st.columns([4,2,4])
with col2:
    if is_plot and db_selected==db_plot:
        if st.button("Plot Games"):     # button in center column
            switch_page('Overall')


# Styling on Tabs
css = '''
div.stTabs {
    min-height: 20vh;  # Minimum height set for the chat area
    max-height: 60vh;  # Maximum height, after which scrolling starts
    overflow-y: auto;  # Allows scrolling when content exceeds max height
    overflow-x: hidden;
}
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
