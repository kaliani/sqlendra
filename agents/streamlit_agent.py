import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.general_tools import QueryResourceTool, CreateQueryTool, SQLQueryRunnerTool

from dotenv import load_dotenv
load_dotenv()

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT= os.getenv("LANGCHAIN_PROJECT")

st.set_page_config(page_title="SQL Query Assistant", page_icon="🤖") 

st.title("SQL Query Assistant")

st.markdown("This assistant can help generate SQL queries from natural language question!")

tools = [QueryResourceTool(), CreateQueryTool(), SQLQueryRunnerTool()]
llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0)
conversational_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=1, return_messages=True)

query_agent = initialize_agent(agent='chat-conversational-react-description', 
                                  tools=tools, 
                                  llm=llm, 
                                  verbose=True, 
                                  max_iterations=3, 
                                  early_stopping_method='generate',
                                  handle_parsing_errors=True, 
                                  memory=conversational_memory)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = query_agent.run(prompt, callbacks=[st_callback])
        st.write(response)

st.markdown("---")