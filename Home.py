import streamlit as st
import pandas as pd
import os
import random
import time
from module.__custom__ import *
from streamlit_extras.switch_page_button import switch_page
df = pd.read_csv('./data/cosine.csv')

with open( ".\css\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


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

with st.sidebar: is_plot = st.toggle('Enable Plot')
db_selected = db_cos
if is_plot: db_selected = db_plot


##### Conversational Retrieval #####
from langchain.agents.agent_toolkits.conversational_retrieval.tool import (
    create_retriever_tool,
)
retriever = db_selected.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "document-retriever",
    "Query a retriever to get information about the video game dataset.",
)
##################################


##### Retriever - Self Query #####
metadata_field_info = [
    AttributeInfo(
        name="name",
        description="The name of the video game on steam",
        type="string",
    )
]
document_content_description = "Brief summary of a video game on Steam"

retriever_plot = SelfQueryRetriever.from_llm(
    llm,
    db_selected,
    document_content_description,
    metadata_field_info,
    enable_limit=True, 
)
##################################


from typing import List
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from pydantic import BaseModel, Field


class Response(BaseModel):
    """Final response to the question being asked.
        If you do not have an answer, say you do not have an answer, and ask the user to ask another recommendation.
        If you do have an answer, be verbose and explain why you think the game answers the user's query.
        Don't give information not mentioned in the documents CONTEXT.
        You should always refuse to answer questions that are not related to this specific domain, of video game recommendation.
        If no document passes the minimum threshold of similarity .75, default to apologizing for no answer.
    """

    answer: str = Field(description="The final answer to the user, including the names in the answer.")
    name: List[str] = Field(
        description="A list of the names of the games found for the user. Only include the game name if it was given as a result to the user's query."
    )


import json
from langchain.schema.agent import AgentActionMessageLog, AgentFinish
def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a recommendation assistant, based off documents."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(
    functions=[
        # The retriever tool
        format_tool_to_openai_function(retriever_tool),
        # Response schema
        convert_pydantic_to_openai_function(Response),
    ]
)

agent = (
    {
        "input": lambda x: x["input"],
        # Format agent scratchpad from intermediate steps
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | parse
)
agent_executor = AgentExecutor(tools=[retriever_tool], agent=agent, verbose=True)

post_prompt = """
    1. Respond with a respectable and friendy tone.
    2. You should give the best possible answer based on user's query. 
    3. Do not give me any information that is not included in the document. 
    4. If you are able to, provide the links to the steam site for the games answer.
    5. If you need more context from the user, ask them to provide more context in the next query. Do not include games that contain the queried game in the title.
    6. If a user asks for a type of game, use that type to find a game that mentions the type.
"""
# If you do not have an answer, your response should be kind and apologetic, as to why you do not have an answer. 
# If a user asks for a specific number of games, and you cannot provide that, answer with what games you found and explain why you could not find others.

st.header("🕹️ GameInsightify")
st.header("Your Personal :green[Game Recommender]")
st.image('./data/img/demoGIF.gif')

    # Description for users
st.markdown("""
        Welcome to GameInsightify! This chatbot will help you find the perfect game based on your preferences. 
        Just type in what you're looking for in a game, and let our AI assistant provide recommendations.
        """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'gamenames' not in st.session_state:
    st.session_state.gamenames = []

# Slider on range and button to clear chat history
col1, col2= st.columns([8,2])
with col1: 
    pass
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
        assistant_response = ""
        full_response = ""
        
        # docs = db.max_marginal_relevance_search(prompt,k=query_num, fetch_k=10) # Sending query to db
        if is_plot:
            docs = retriever_plot.invoke(prompt)
            full_response = random.choice(                                          # 1st sentence of response
                ["I recommend the following games:\n",
                f"Hi, human! These are the {len(docs)} best games:\n",
                f"I bet you will love these {len(docs)} games:\n",]
            )
            
            # formatting response from db
            top_games = []   
            for idx, doc in enumerate(docs):
                gamename = doc.metadata['name']
                top_games.append(gamename)
                assistant_response += f"{idx+1}. {gamename}\n"
            
        else:        
            docs = agent_executor.invoke(
                {"input": f"{prompt} {post_prompt}"},
                return_only_outputs=True,
            )                                     # retrieve response from chatgpt
            try:
                assistant_response += docs["answer"]
            except:
                assistant_response += docs["output"]
            top_games = docs['name']
        

        print(docs)

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

col1, col2, col3= st.columns([4,3,4])
with col2:
    if is_plot and db_selected==db_plot:
        if st.button("Plot Games"):     # button in center column
            switch_page('Overall')
    else:
        try:
            appid = df[df['Name']==top_games[0]]['AppID'].iloc[0]
            url = f'https://store.steampowered.com/app/{appid}'
            st.link_button("Check on Steam", url)
        except: pass
with st.sidebar: 
    try: home_dfbox(top_games)
    except: pass

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