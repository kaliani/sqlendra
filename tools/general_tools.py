import os
import sys
from typing import Any, List, Optional, Tuple
import pandas as pd
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.db_utils import create_conn, execute_query
from dotenv import load_dotenv

load_dotenv()

class QueryResourceTool(BaseTool):
    name = "QueryResourceTool"
    description = "Use this tool when you need to calculate the actual execution time of a SQL query in the PostgreSQL database"

    def _run(self, query: str) -> Optional[List[Tuple[Any]]]:
        conn = create_conn()

        if conn is not None:
            analyze_query = f"EXPLAIN ANALYZE {query}"
            result = execute_query(conn, analyze_query)
            conn.close()
            return result
        else:
            print("Error! Cannot create connection to PostgreSQL database server")
            return None
    
    def _arun(self, query: str) -> Optional[List[Tuple[Any]]]:
        return NotImplementedError("This tool does not support asynchronous execution")
    

class CreateQueryTool(BaseTool):
    name = "SQLQueryTool"
    description = "Use this tool when you need to get SQL query from a text description of a user"
    
    def _run(self, message: str):
        chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
        
        main_template = """
                        Based on the table schema below, write a SQL query that would answer the user's question:
                        {engine}
                        ALWAYS USE THE FORMAT INSTRUCTIONS PROVIDED. 
                        Failure to do so will result in a failed task.
                        Only extract the schemas and tables that are explicitly mentioned in the user's question. 
                        Do not extract any additional information beyond what the user has provided. 
                        Always return only a formatted SQL query without any other information or guesswork.
                        Question: {question}"""
        prompt_template = ChatPromptTemplate.from_template(main_template)

        with open("tools/data/schema.txt", "r") as f:
            schema = f.read()

        messages = prompt_template.format_messages(engine=schema, question=message)
        response = chat(messages)
        return response

    
    def _arun(self, message: str):
        raise NotImplementedError("This tool does not support async")
    

class SQLQueryRunnerTool(BaseTool):
    name = "SQLQueryRunnerTool"
    description = "Use this tool when you need to run a SQL query in the PostgreSQL database"

    def _run(self, query: str) -> Optional[List[Tuple[Any]]]:
        conn = create_conn()

        if conn is not None:
            result_data = pd.read_sql(query, conn)
            conn.close()
            result = {"sql_code": query, "result": result_data}
            return result
        else:
            print("Error! Cannot create connection to PostgreSQL database server")
            return None
    
    def _arun(self, query: str) -> Optional[List[Tuple[Any]]]:
        return NotImplementedError("This tool does not support asynchronous execution")