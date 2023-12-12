# %%
import pandas as pd
from langchain.vectorstores import Chroma
import os
import openai
import sys
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate 
from langchain.embeddings.openai import OpenAIEmbeddings
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
    api_key = read_api_key_from_secrets()
    print(f"OpenAI API Key Found")
except (FileNotFoundError, ValueError, KeyError) as e:
    print(f"Error: {e}")
llm = OpenAI(openai_api_key=f"{api_key}")
openai.api_key  = f"{api_key}"
os.environ['OPENAI_API_KEY'] = f"{api_key}"

template = """Question: {question}

Answer: Describe in full detail"""

prompt = PromptTemplate(template=template, input_variables=["question"])

persist_directory = 'docs/chroma'

embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory,embedding_function=embedding)


llm_name = "gpt-3.5-turbo"

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)

from langchain.agents.agent_toolkits.conversational_retrieval.tool import (
    create_retriever_tool,
)
retriever = vectordb.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "state-of-union-retriever",
    "Query a retriever to get information about state of the union address",
)

from typing import List

from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from pydantic import BaseModel, Field


class Response(BaseModel):
    """Final response to the question being asked."""

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
        ("system", "You are a helpful document assistant"),
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

def getRecommendations(query : str):
    result = agent_executor.invoke(
        {"input": f"{query}"},
        return_only_outputs=True,
    )
    return result


# res = getRecommendations("Give me 5 games that have zombies and guns.")
# print(res['answer'])
# print(res['name'])