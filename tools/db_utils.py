
from typing import List, Tuple, Any
import psycopg2
from psycopg2 import Error

## define conn variables
def create_conn() -> psycopg2.extensions.connection:
    conn = None
    try:
        conn = psycopg2.connect(
            user="postgres",
            password="MakeSomeNoise1",
            host="192.168.0.100",
            port="5432",
            database="postgres"
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