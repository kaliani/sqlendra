
import os
from typing import List, Tuple, Any
import psycopg2
from psycopg2 import Error

## define conn variables
def create_conn() -> psycopg2.extensions.connection:
    conn = None
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")
    return conn

def execute_query(conn, query) -> List[Tuple[Any]]:
    records = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
    except Error as e:
        print(f"Error executing query: {e}")
    return records