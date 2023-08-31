import sys
import os
from langsmith import Client
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.general_tools import QueryResourceTool, CreateQueryTool, SQLQueryRunnerTool
from dotenv import load_dotenv

load_dotenv()

tools = [QueryResourceTool(), CreateQueryTool(), SQLQueryRunnerTool()]
llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0)

def create_query_agent():
    conversational_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=1, input_key='input',  output_key='output',return_messages=True)
    return initialize_agent(agent='chat-conversational-react-description', 
                            tools=tools, 
                            llm=llm, 
                            verbose=True, 
                            max_iterations=3, 
                            early_stopping_method='generate',
                            handle_parsing_errors=True, 
                            memory=conversational_memory)


client = Client()

eval_config = RunEvalConfig(
    evaluators=[
        "cot_qa"
    ],
)
chain_results = run_on_dataset(
    client,
    dataset_name="second_dataset",
    llm_or_chain_factory=create_query_agent,
    evaluation=eval_config
)